import requests
import pandas as pd
import uuid
from time import sleep
from random import randint
import re

def extract_company_data(symbols, output_dir, api_key):
    df = pd.DataFrame(columns=['stock_symbol','company_name', 'industry'])
    for raw_sym in symbols:
        symbol = raw_sym.replace("/", "-")
        symbol = re.sub(r"\^[A-Z]$", "", symbol)
        url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error retrieving data for {symbol}")
            continue
        data = response.json()
        if len(data) == 0:
            data = {
                'stock_symbol': raw_sym,
                'company_name': 'Unknown',
                'industry': 'unknown'
            }
            df = pd.concat([df, pd.DataFrame.from_dict({k:[v] for k,v in data.items()})], ignore_index=True)
            continue
        company = data[0]
        if 'industry' in company:
            company_name = company['companyName']
            industry = company['industry']
            data = {
                'stock_symbol': raw_sym,
                'company_name': company_name,
                'industry': industry
            }
            df = pd.concat([df, pd.DataFrame.from_dict({k:[v] for k,v in data.items()})], ignore_index=True)
        sleep(randint(1,3))
    out_path = f'{output_dir}/company_size_data_{str(uuid.uuid4()).split("-")[0]}.csv'
    output = df.to_csv(out_path, index=False)
    return out_path

# symbols = ['AAPL', 'GOOGL', 'MSFT']
# api_key = ""
# symbols = pd.read_csv("warn-155.csv")["Symbol"].to_list()
# output_dir = './'
# extract_company_data(symbols, output_dir, api_key)
