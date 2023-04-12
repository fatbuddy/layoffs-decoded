import requests
import pandas as pd
import re
import uuid
from random import randint
from time import sleep

def extract_company_data(symbols, output_dir, start_year, end_year, api_key, quarterly=False):
    df = pd.DataFrame(columns=['stock_symbol', 'company_name', 'period_of_report', 'employee_count'])
    for raw_sym in symbols:
        symbol = raw_sym.replace("/", "-")
        symbol = re.sub(r"\^[A-Z]$", "", symbol)
        url = f'https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error retrieving data for {symbol} - status_code {response.status_code}")
            continue
        data = response.json()
        for item in data:
            period_of_report = item['periodOfReport']
            year = int(period_of_report[:4])
            if start_year <= year <= end_year:
                if quarterly:
                    for i in ['01','04','08','12']:
                        # Append the row 4 times for each quarter
                        row_data = {
                            'stock_symbol': raw_sym,
                            'company_name': item['companyName'],
                            'period_of_report': period_of_report[:5]+i+period_of_report[7:],
                            'employee_count': item['employeeCount']
                        }
                        df = pd.concat([df, pd.DataFrame.from_dict({k:[v] for k,v in row_data.items()})], ignore_index=True)
                else:
                    # Append the row once
                    row_data = {
                            'stock_symbol': raw_sym,
                            'company_name': item['companyName'],
                            'period_of_report': period_of_report,
                            'employee_count': item['employeeCount']
                        }
                    df = pd.concat([df, pd.DataFrame.from_dict({k:[v] for k,v in row_data.items()})], ignore_index=True)
        sleep(randint(1,3))
    if quarterly == True:
        out_path = f'{output_dir}/company_size_data_quarterly_{str(uuid.uuid4()).split("-")[0]}.csv'
    else:
        out_path = f'{output_dir}/company_size_data_{str(uuid.uuid4()).split("-")[0]}.csv'
    output = df.to_csv(out_path, index=False)
    return out_path
