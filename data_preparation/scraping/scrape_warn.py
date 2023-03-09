import requests 
import pandas as pd
import time
import re

API_KEY = "DEO388ZM3UEZ34M8"
ALPHA_VANTAGE_URL="https://www.alphavantage.co/query"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

def getSymbol(company_name, apikey):
    res = requests.get(
        url=ALPHA_VANTAGE_URL, 
        params={
            'function': 'SYMBOL_SEARCH',
            'keywords': company_name,
            'apikey': apikey
        },
        headers={'User-Agent': USER_AGENT}
    )
    try :
        data = res.json()
    except:
        return None
        
    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        us_equity = list(filter(lambda d: d['4. region'] == 'United States', data['bestMatches']))
        if len(us_equity) > 0:
            return us_equity[0]['1. symbol']
        return None
    else:
        return None

# def read_warn_company_names(warn_csv_path):
#     df = pd.read_csv()
#     return df['Company'].tolist()


# result = getSymbol(re.sub(r'[^\w]', ' ', "Microsoft"), API_KEY)
# print("Result ", result)