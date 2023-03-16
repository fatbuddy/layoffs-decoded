import os
import pandas as pd
import csv
import re
# Define the folder containing the CSV files
folder_path = 'csv/employee_csv_20230315'

# Create an empty list to store the first row of each CSV file
first_rows = []

empty_field_threshold = 2
# if the first column more than 50 character it is not likely to be column
len_character_threshold = 50

# Define a regular expression pattern to match HTML tags
html_tag_pattern = re.compile(r'<\s*(html|head|body|table)\b[^>]*>', re.IGNORECASE)

min_num_cols = 5

invalid_first_row_count = 0
invalid_file_count = 0

employee_count = 0

def preprocess_file(folder_name, filename):
    rows = []
    columns = []
    print("Opening file: "+filename)
    # Open the CSV file
    with open(os.path.join(folder_name, filename), 'r', encoding='utf-8') as csvfile:
        # Read the entire contents of the CSV file as a string
        file_content = csvfile.read()
        # Check if the file contains any HTML tags
        if re.search(html_tag_pattern, file_content):
            # Skip to the next file if the file contains HTML content
            print(f"HTML element found in file {filename} Skipping")
            return 0
        csvfile.seek(0)  # move file pointer to start of file
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',')
        try:
            foundColumn = False
            # Get the first row of the CSV file
            while True:
                first_row = next(reader)
                # hard code for the case BigCommerce
                if "BigCommerce" in filename:
                    first_row = next(reader)

                if len_character_threshold <= len(first_row[0]):
                    # Skip to the next row
                    # print(f"too many characters in file {filename}: skip ")
                    # invalid_first_row_count += 1
                    continue

                # Check if the first row contains column names
                if sum([1 for colname in first_row if not colname]) <= empty_field_threshold and len(first_row) >= min_num_cols:
                    # Append the first row to the list of first rows
                    columns = first_row
                    foundColumn = True
                    break

                    # Skip to the next row
                    # invalid_first_row_count += 1
            if foundColumn:
                while True:
                    row = next(reader)
                    if len(row) == len(columns):
                        if sum([1 for colname in row if not colname]) == len(columns):
                            print("skip row")
                            continue
                        rows.append(row)
                    else:
                        print("Found #column does not match #row")
                        continue
                    pass
        except StopIteration as e:
            print(f"Reached end of file: {filename}")
            # Skip this file if it has less than one row
            if len(columns) > 0:
                df = pd.DataFrame(rows, columns=columns)
                df.to_csv('output/'+filename)
            return len(rows)
        except Exception as e:
            print(f"Exception error file not valid: {e} in {filename}")
            return 0
    # Write the list of first rows to a text file
    # with open('output.txt', 'w') as txtfile:
    #     for row in first_rows:
    #         # Write the filename and first row to the text file separated by a comma
    #         txtfile.write(row[0] + ',' + ','.join(row[1]) + '\n')

    # print("invalid_first_row_count: " + str(invalid_first_row_count))
    # print("invalid_file_count: " + str(invalid_file_count))
    print(first_rows)

for filename in os.listdir(folder_path):
    print(filename)
    count = preprocess_file('csv/employee_csv_20230315', filename)
    employee_count += count
    print(count)

print(f"Toal Count: {employee_count}")