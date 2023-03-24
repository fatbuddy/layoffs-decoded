import requests
import pandas as pd

def extract_company_data(symbols, output_dir, api_key):
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
    out_path = f'{output_dir}/company_industry.csv'
    output = df.to_csv(out_path, index=False)
    return out_path

# symbols = ['AAPL', 'GOOGL', 'MSFT']
# api_key = ""
# symbols = pd.read_csv("warn-155.csv")["Symbol"].to_list()
# output_dir = './'
# extract_company_data(symbols, output_dir, api_key)
