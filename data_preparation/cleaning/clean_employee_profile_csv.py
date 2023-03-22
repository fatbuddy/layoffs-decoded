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

def detect_interested_label(labels: list[str]):
    """
    Detect labels of interested, i.e ["name or email (as ID)", "title/role", "department/area/function", "location"]
    """
    title_regex = re.compile(r".*(title|role|position|domain).*", flags=re.IGNORECASE)
    function_regex = re.compile(r".*(department|area|function|team|discipline).*", flags=re.IGNORECASE)
    location_regex = re.compile(r".*(location).*", flags=re.IGNORECASE)
    desired_label_regex = re.compile(r".*(interest|desire|prefer|open).*", flags=re.IGNORECASE)
    title_label = None
    desired_title_label = None
    function_label = None
    desired_function_label = None
    location_label = None
    desired_location_label = None
    for label in labels:
        if title_regex.match(label):
            if desired_label_regex.match(label):
                desired_title_label = label
            else:
                title_label = label
        elif function_regex.match(label):
            if desired_label_regex.match(label):
                desired_function_label = label
            else:
                function_label = label
        elif location_regex.match(label):
            if desired_label_regex.match(label):
                desired_location_label = label
            else:
                location_label = label
            # possible_title_labels.append(label)
            # print(f"possible title lable: {label}")
    if title_label is None and desired_title_label:
        title_label = desired_title_label
    if function_label is None and desired_function_label:
        function_label = desired_function_label
    if location_label is None and desired_location_label:
        location_label = desired_location_label
    # label_list = [title_label, function_label, location_label]
    # return label_list
    label_map = {
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
    # Write the list of first rows to a text file
    # with open('output.txt', 'w') as txtfile:
    #     for row in first_rows:
    #         # Write the filename and first row to the text file separated by a comma
    #         txtfile.write(row[0] + ',' + ','.join(row[1]) + '\n')

    # print("invalid_first_row_count: " + str(invalid_first_row_count))
    # print("invalid_file_count: " + str(invalid_file_count))
    # print(first_rows)

# for filename in os.listdir(folder_path):
#     print(filename)
#     count = preprocess_file('csv/employee_csv_20230315', filename)
#     employee_count += count
#     print(count)

# print(f"Toal Count: {employee_count}")