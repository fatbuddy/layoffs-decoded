import pandas as pd
from tqdm import tqdm
import re
import s3fs

AWS_S3_BUCKET = "layoffs-decoded-master"
AWS_S3_PREFIX = "training_data_q3"
AWS_ACCESS_KEY_ID = "AKIAUHN3JA72IHF7WP6J"
AWS_SECRET_ACCESS_KEY = "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"

## 3_token_department_combiner
#
# This file will combine the department tokens given from GPT (departments_tokens.txt)
# so that we can identify the function token correspond to department
# the output will be the list of department attached back with standardized title

fs = s3fs.S3FileSystem(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)
with fs.open(f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/departments_tokens.txt", 'r') as f:
    # read the input file and split the data by newline
    data = f.read().split('\n')

# create an empty list to store department and token data
dept_data = []

# loop through each line in the data and split the department and tokens
for line in data:
    if line:
        dept, tokens = line.split(": ")
        tokens = tokens.split(", ")
        for token in tokens:    
            # append the department and token data as a tuple to the dept_data list
            dept_data.append((token, dept))


# create a pandas dataframe from the dept_data list
df_token_department = pd.DataFrame(dept_data, columns=["tokens", "department"])
df_token_department.to_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/df_token_department.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },index=False)


# using the token matched with department, and merge it with the standardize title token
employee_df = pd.read_csv(
    f"s3://{AWS_S3_BUCKET}/{AWS_S3_PREFIX}/function_token_matching.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },
)
employee_df_merge = pd.merge(employee_df, df_token_department, left_on="matched_token", right_on="tokens", how="left")

# Using the token matching from the non-empty function for department
# Loop over the rows in the employee DataFrame
for i, row in tqdm(employee_df_merge.iterrows()):
    # Get the depmartment from the current row
    department = str(row['department'])
    if not employee_df_merge['department'].isna()[i]:
        continue
    if employee_df_merge['function'].isna()[i]:
        continue
    function = str(row['function']).lower()
    # function = function.split('/')
    function = re.findall(r'[a-zA-Z0-9]+', str(function).lower())
    # Loop over the rows in the filtered gazetteer DataFrame
    for j, df_row in df_token_department.iterrows():
        # Get the keyword from the current gazetteer row
        keyword = df_row['tokens'].lower()
        found = False
        # Check if any of the title words match the keyword
        if any(word.strip().lower() == keyword for word in function):
            # If a match is found, add it to the matched tokens list
            employee_df_merge.at[i, 'department'] = df_token_department.at[j, 'department']
            found = True
            break
        if found:
            break

employee_df_merge['department'] = employee_df_merge['department'].fillna("Others")

department_counts = employee_df_merge.groupby('department').size().reset_index(name='count')
# sort the department counts in descending order
department_counts = department_counts.sort_values('count', ascending=False)

# rename the columns to "name" and "count"
department_counts = department_counts.rename(columns={'department': 'name', 'count': 'value'})
department_counts.to_csv(
    f"s3://{AWS_S3_BUCKET}/feature_reults/q3_departments_counts/department_counts.csv",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY
    },index=False)