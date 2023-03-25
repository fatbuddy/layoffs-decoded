import csv

# define a function to check if a name is valid
def is_valid_name(name):
    keywords = ['delete'] # list of keywords to avoid in a name
    if not name:
        return True
    if any(keyword in name.lower() for keyword in keywords):
        return False
    if any(char.isdigit() for char in name):
        return False
    if len(name) < 2:
        return False
    return True

def is_valid_email(row, email):
    keywords = ['linkedin', 'gmail']
    if any(keyword in email.lower() for keyword in keywords):
        return True
    if row['email'] and '@' not in row['email']:
        return False
    return True


def validate_csv(input_path, output_dir):
    # open the input file
    with open(input_path, newline='', encoding='utf-8') as infile:

        # create a csv reader object
        reader = csv.DictReader(infile)

        # create a dictionary to store the non-empty name/email values for each source
        sources = {}

        # create a list to store the cleaned data
        cleaned_data = []

        # initialize variables to keep track of removed rows
        invalid_email_count = 0
        invalid_name_count = 0
        empty_row_count = 0
        duplicate_row_count = 0

        # loop through each row in the input file
        for i, row in enumerate(reader):

            # check for empty rows
            if not any(row.values()):
                empty_row_count += 1
                continue

            # check for rows with both name and email empty
            if not row['name'] and not row['email']:
                empty_row_count += 1
                continue

            # check email validity
            if not is_valid_email(row, row['email']):
                invalid_email_count += 1
                continue

            # check name validity
            if row['name'] and not is_valid_name(row['name']):
                invalid_name_count += 1
                continue

            

            # fill empty function values with the previous value in the same source group
            if not row['function']:
                if cleaned_data and row['source'] == cleaned_data[-1]['source']:
                    row['function'] = cleaned_data[-1]['function']

            # check for duplicate rows
            source = row['source']
            name = row['name']
            email = row['email']
            if source in sources:
                if name and name in sources[source]['names']:
                    duplicate_row_count += 1
                    print(row)
                    continue
                if email and email in sources[source]['emails']:
                    duplicate_row_count += 1
                    print(row)
                    continue
            sources.setdefault(source, {'names': set(), 'emails': set()})
            sources[source]['names'].add(name)
            sources[source]['emails'].add(email)

            # append the cleaned row to the list
            cleaned_data.append(row)

        # print the number of removed rows
        print(f'{empty_row_count} empty rows were removed.')
        print(f'{invalid_email_count} rows with invalid email were removed.')
        print(f'{invalid_name_count} rows with invalid name were removed.')
        print(f'{duplicate_row_count} duplicate rows were removed.\n')

        print(f'Total invalid records removed: {duplicate_row_count + empty_row_count + invalid_email_count +invalid_name_count}')

        # write the cleaned data to a new CSV file
        with open(f"{output_dir}/employee_merged_csv.csv", 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=cleaned_data[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_data)
    return f"{output_dir}/employee_merged_csv.csv"