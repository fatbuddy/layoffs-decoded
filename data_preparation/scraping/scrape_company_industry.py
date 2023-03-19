import requests
import pandas as pd

def extract_company_data(symbols, api_key):
    df = pd.DataFrame(columns=['stock_symbol','company_name', 'industry'])
    for symbol in symbols:
        url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error retrieving data for {symbol}")
            continue
        data = response.json()
        company_name = data[0]['companyName']
        industry = data[0]['industry']
        df = df.append({
            'stock_symbol': symbol,
            'company_name': company_name,
            'industry': industry
        }, ignore_index=True)
    df.to_csv('company_industry.csv', index=False)

symbols = ['AAPL', 'GOOGL', 'MSFT']
api_key = '6b5ead8d3c6bceb25d50bc6237dc8543'
extract_company_data(symbols, api_key)
