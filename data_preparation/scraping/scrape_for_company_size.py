import requests
import pandas as pd

def extract_employee_data(symbols, start_year, end_year, api_key):
    df = pd.DataFrame(columns=['company_name', 'period_of_report', 'employee_count'])
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
                df = df.append({
                    'company_name': item['symbol'],
                    'period_of_report': period_of_report,
                    'employee_count': item['employeeCount']
                }, ignore_index=True)
    df.to_csv(f'company_size_data.csv', index=False)

symbols = ['AAPL', 'GOOGL', 'MSFT']
start_year = 2018
end_year = 2020
api_key = "6b5ead8d3c6bceb25d50bc6237dc8543"
extract_employee_data(symbols, start_year, end_year, api_key)
