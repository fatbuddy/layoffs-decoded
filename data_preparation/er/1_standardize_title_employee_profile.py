import pandas as pd
import re
from tqdm import tqdm
import s3fs

AWS_S3_BUCKET = "layoffs-decoded-master"
AWS_S3_PREFIX = "training_data_q3"
AWS_ACCESS_KEY_ID = "AKIAUHN3JA72IHF7WP6J"
AWS_SECRET_ACCESS_KEY = "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"

## 1_standardize_title_employee_profile
#
# This file will take the input from employee profile we scraped
# and find the nearest match with list of alternative titles from onetcenter.org
# by 2 stages of ER (jaccard) score > 0.35

# 1st stage of ER will be working on full title
# 2nd stage of ER will duel with title with short form (ie, CEO, SDE, etc)

jaccard_threshold = 0.35

emp_df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/employee_merged_validated_csv.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },
)

# Load the alternate_titles.csv file
alt_df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/alternate_titles.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },
)

# Create a new column in emp_df to hold the matching alternate titles
emp_df['matching_title'] = ''

# Define the Jaccard similarity function
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def getLargestLengthTitle(titles):
    max_len = 0
    result = ''
    for title in titles:
        if  len(title) > max_len:
            max_len = len(title)
            result = title.strip()
    return result

# Create an empty DataFrame to hold the matching titles
result_df = pd.DataFrame(columns=['source', 'function', 'title', 'cloest_title', 'matching_title'])

# Iterate through each row in emp_df
for index, row in tqdm(emp_df.iterrows()):
    # Get the title for the current row
    title = str(row['title'])
    lower_title = title.lower()
    matching_title = ''
    # put the unknown title
    if not title:
        entry = pd.DataFrame({'source': row['source'], 'function': row['function'], 'title': lower_title, 'matching_title': 'Unknown'}, index=[0])
        result_df = pd.concat([result_df.loc[:], entry]).reset_index(drop=True)
        continue
    # Iterate through each row in alt_df
    max_jaccard = 0
    
    # split the string by / , and taking the longest one to process
    splited_titles = lower_title.split('/')
    lower_title = getLargestLengthTitle(splited_titles)
    
    for alt_title in alt_df['Alternate Title']:
        # Calculate the Jaccard similarity between the current title and the alternate title
        title_words = re.findall(r'[a-zA-Z0-9]+', str(title).lower())
        alt_title_words = re.findall(r'[a-zA-Z0-9]+', str(alt_title).lower())
        jaccard = jaccard_similarity(title_words, alt_title_words)
        # If the Jaccard similarity is greater than the current maximum, update the maximum and set the matching_title
        if jaccard > max_jaccard:
            max_jaccard = jaccard
            matching_title = alt_title
    if max_jaccard >= jaccard_threshold:
        # Add a new row to the result_df DataFrame with the title and matching_title
        entry = pd.DataFrame({'source': row['source'],
                              'name':row['name'],
                              'function': row['function'],
                              'title': title,
                              'jaccard_score': max_jaccard,
                              'matching_title': matching_title}, index=[0])
        result_df = pd.concat([result_df.loc[:], entry]).reset_index(drop=True)
        continue
    max_short_title_jaccard = 0
        
    for short_title in alt_df['Short Title']:
        # Check if Short Title column is not empty and the Jaccard score is greater than or equal to 0.7
        if pd.notna(short_title):
            # Calculate the Jaccard similarity between the current title and the short title
            title_words = re.findall(r'[a-zA-Z0-9]+', lower_title)
            short_jaccard = jaccard_similarity(title_words, short_title.lower().split())
            # If the Jaccard similarity of the short title is greater than the current maximum
            # and greater than or equal to the threshold, update the maximum and set the matching_title
            if short_jaccard > max_short_title_jaccard:
                max_short_title_jaccard = short_jaccard
                matching_title = short_title
    if max_short_title_jaccard >= 0.35:
        # Add a new row to the result_df DataFrame with the title and matching_title
        entry = pd.DataFrame({'source': row['source'], 
                              'name':row['name'],
                              'function': row['function'],
                              'title': title, 
                              'jaccard_score': max_short_title_jaccard, 
                              'matching_title': alt_title}, index=[0])
        result_df = pd.concat([result_df.loc[:], entry]).reset_index(drop=True)
    else:
        # mark it to Unknown title if not regonize
        entry = pd.DataFrame({'source': row['source'], 
                              'name':row['name'],
                              'function': row['function'],
                              'title': title, 
                              'jaccard_score': max(max_jaccard, max_short_title_jaccard),
                              'cloest_title': matching_title,
                              'matching_title': 'Unknown'}, index=[0])
        result_df = pd.concat([result_df.loc[:], entry]).reset_index(drop=True)

# Save the result_df DataFrame as a CSV file
result_df.to_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/standardize_title_employee_profile_csv.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },index=False)

title_counts = result_df.groupby('matching_title').size().reset_index(name='count')
# sort the department counts in descending order
title_counts = title_counts.sort_values('count', ascending=False)
# rename the columns to "name" and "count"
title_counts = title_counts.rename(columns={'matching_title': 'name', 'count': 'value'})
title_counts.to_csv(
    f"s3://{AWS_S3_BUCKET}/feature_reults/q3_titles_counts/titles_counts.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },index=False)