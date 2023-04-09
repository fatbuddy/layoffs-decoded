import pandas as pd
import re
from tqdm import tqdm
import csv
import s3fs

AWS_S3_BUCKET = "layoffs-decoded-master"
AWS_S3_PREFIX = "training_data_q3"
AWS_ACCESS_KEY_ID = "AKIAUHN3JA72IHF7WP6J"
AWS_SECRET_ACCESS_KEY = "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"

## 2_function_token_matching
#
# This file will take the input from previous stage (standardize_title)
# so that we can extract the function keyword from the title
# the function token can be found from https://github.com/junhua/IPOD
# the output will be the standardized title with assoicate function token into a csv file

# Read in the employee CSV file
employee_df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/standardize_title_employee_profile_csv.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },
)
# Read in the gazetteer CSV file
gazetteer_df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/gazetteer.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },
)

# Filter the gazetteer to only include rows with 'FUN' in A1, A2, or A3
filtered_gazetteer_df = gazetteer_df[
    (gazetteer_df['A1'] == 'FUN') |
    (gazetteer_df['A2'] == 'FUN') |
    (gazetteer_df['A3'] == 'FUN')
]

# Create an empty list to hold the matched tokens
matched_tokens = []

# Loop over the rows in the employee DataFrame
for i, row in tqdm(employee_df.iterrows()):
    # Get the title from the current row
    title = str(row['matching_title'])

    # Split the title string into a list of words using regular expressions
    title_words = re.findall(r'\w+', title.lower())
    
    # Loop over the rows in the filtered gazetteer DataFrame
    for j, gaz_row in filtered_gazetteer_df.iterrows():
        # Get the keyword from the current gazetteer row
        keyword = gaz_row['Title'].lower()
        found = False
        # Check if any of the title words match the keyword
        if any(word == keyword for word in title_words):
            # If a match is found, add it to the matched tokens list
            employee_df.at[i, 'matched_token'] = keyword
            found = True
            break
        if found:
            break

token = set(employee_df['matched_token'].unique())
employee_df.to_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/function_token_matching.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },index=False)