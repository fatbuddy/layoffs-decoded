import requests
import pandas as pd

symbol = 'AAPL'
api_key = "6b5ead8d3c6bceb25d50bc6237dc8543"

url = f'https://financialmodelingprep.com/api/v3/company/profile/{symbol}?apikey={api_key}'
response = requests.get(url)

data = response.json()
# print(response.json())

company_data = data['profile']

employees = company_data['fullTimeEmployees']

company_df = pd.DataFrame({'symbol': [symbol],
                           'employees': [employees]})

print(company_df)
# company_df.to_csv(f'{symbol}_data.csv', index=False)
