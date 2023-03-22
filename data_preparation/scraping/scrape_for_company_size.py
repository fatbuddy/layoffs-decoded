import requests
import pandas as pd

def extract_company_data(symbols, output_dir, start_year, end_year, api_key, quarterly=False):
    df = pd.DataFrame(columns=['stock_symbol', 'company_name', 'period_of_report', 'employee_count'])
    for symbol in symbols:
        url = f'https://financialmodelingprep.com/api/v4/historical/employee_count?symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error retrieving data for {symbol}")
            continue
        data = response.json()
        for item in data:
            period_of_report = item['periodOfReport']
            year = int(period_of_report[:4])
            if start_year <= year <= end_year:
                row_data = {
                    'stock_symbol': item['symbol'],
                    'company_name': item['companyName'],
                    'period_of_report': period_of_report,
                    'employee_count': item['employeeCount']
                }
                if quarterly:
                    # Append the row 4 times for each quarter
                    for i in range(1, 5):
                        df = df.append(row_data, ignore_index=True)
                else:
                    # Append the row once
                    df = df.append(row_data, ignore_index=True)
    output = df.to_csv(f'{output_dir}/company_size_data.csv', index=False)
    return f'{output_dir}/company_size_data.csv'
# symbols = ['AAPL', 'GOOGL', 'MSFT']
# start_year = 2018
# end_year = 2020
# api_key = "6b5ead8d3c6bceb25d50bc6237dc8543"
# extract_company_data(symbols, start_year, end_year, api_key, quarterly=False)