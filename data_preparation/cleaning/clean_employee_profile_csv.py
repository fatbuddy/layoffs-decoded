import os
import pandas as pd
import csv
import re

# Create an empty list to store the first row of each CSV file
first_rows = []

# if the first column more than 50 character it is not likely to be column
len_character_threshold = 50

# Define a regular expression pattern to match HTML tags
html_tag_pattern = re.compile(r'<\s*(html|head|body|table)\b[^>]*>', re.IGNORECASE)

invalid_first_row_count = 0
invalid_file_count = 0
employee_count = 0

def match_label(to_match, labels):
    match_regex = re.compile(f".*({to_match}).*", flags=re.IGNORECASE)
    desired_regex = re.compile(r".*(interest|desire|prefer|open).*", flags=re.IGNORECASE)
    matched_label = None
    desired_label = None
    for label in labels:
        if match_regex.match(label):
            if desired_regex.match(label):
                desired_label = label
            else:
                matched_label = label
    if matched_label is None and desired_label:
        matched_label = desired_label
    return matched_label

def detect_interested_label(labels: list[str]):
    """
    Detect labels of interested, i.e ["name or email (as ID)", "title/role", "department/area/function", "location"]
    """
    title_label = match_label("title|role|position|domain", labels)
    function_label = match_label("department|area|function|team|discipline", labels)
    city_label = match_label("city", labels)
    country_label = match_label("country", labels)
    location_label = match_label("location", labels)
    name_label = match_label("location", labels)
    location_label = city_label or country_label or location_label
    # label_list = [title_label, function_label, location_label]
    # return label_list
    label_map = {
        "name": name_label,
        "title": title_label,
        "function": function_label,
        "location": location_label
    }
    return label_map

def clean_csv(input_file, output_dir):
    rows = []
    labels = []
    print(f"Opening file: {input_file}")
    # Open the CSV file
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        # Read the entire contents of the CSV file as a string
        file_content = csvfile.read()

        # Check if the file contains any HTML tags
        if re.search(html_tag_pattern, file_content):
            # Skip to the next file if the file contains HTML content
            print(f"skipping: HTML element found in file {input_file}")
            return None

        csvfile.seek(0)  # move file pointer to start of file
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',')
        try:
            # Get the first row of the CSV file
            while len(labels) == 0:
                current_row = next(reader)
                if len_character_threshold <= len(current_row[0]):
                    print("skipping: too many characters in first row cell")
                    print(current_row[0])
                    continue

                row_text = "|".join(current_row).lower()
                if row_text.find("name") != -1 or \
                    row_text.find("nome") != -1 or \
                    row_text.find("nombre") != -1:
                    labels = current_row

            print(f"label row found: {labels}")
            intereted_labels = detect_interested_label(labels=labels)
            for k, v in intereted_labels.items():
                if v is not None:
                    idx = [i for i in range(0, len(labels)) if labels[i]==v]
                    if len(idx) > 0:
                        labels[idx[0]] = k
            while True:
                row = next(reader)
                if len(row) <= len(labels):
                    if "".join(row).strip() == "":
                        print("skipping empty row")
                        continue
                    rows.append(row)
                else:
                    rows.append(row[:len(labels)])
        except StopIteration as e:
            print(f"Reached end of file: {input_file}")
            # Skip this file if it has less than one row
            if len(labels) > 0 and len(rows) > 0:
                df = pd.DataFrame(rows, columns=labels)
                output_file = input_file.split('/')[-1].split('.')[0]
                output_path = f"{output_dir}/{output_file}-cleaned.csv"
                print(f"writing output file to {output_path}")
                df.to_csv(output_path)
                return output_path
            return None
        except Exception as e:
            print(f"Exception error file not valid: {e} in {input_file}")
            return None

def combine_csv(inputs, output_dir):
    combined_df = pd.DataFrame(columns=['name','title','function','location'])
    for f in inputs:
        csv_df = extract_csv(f)
        if csv_df is not None:
            pd.concat([combined_df, csv_df], ignore_index=True)
    combined_df.to_csv(f"{output_dir}/employee_merged_csv.csv")

def extract_csv(input_file):
    df = pd.read_csv(input_file)
    found = [i for i in range(0, len(df.columns)) \
        if df.columns[i]=='title' or df.columns[i]=='location' or df.columns[i]=='function']
    if len(found) == 3:
        extracted_df = df[['title','location','function']]
        return extracted_df
    return None