import requests 
import pandas as pd
import time
import re

API_KEY = ""
ALPHA_VANTAGE_URL="https://www.alphavantage.co/query"
YAHOO_FINANCE_URL="https://query2.finance.yahoo.com/v1/finance/search"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

def clean_company_name(company_name):
    company_name_lower = company_name.lower()
    return re.sub(r',?\s*(llc|inc|co)\.?$', '', company_name_lower)

def getSymbol(company_name, apikey):
    res = requests.get(
        url=ALPHA_VANTAGE_URL, 
        params={
            'function': 'SYMBOL_SEARCH',
            'keywords': clean_company_name(company_name),
            'apikey': apikey
        },
        headers={'User-Agent': USER_AGENT}
    )
    if res.status_code != 200:
        raise ValueError(f"Response status: {res.status_code}. {res.text}")
    try :
        data = res.json()
    except:
        return None
        
    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        # return data['bestMatches'][0]['1. symbol']
        us_equity = list(filter(
            lambda d: (d['8. currency'] == 'USD' and d['3. type'] == 'Equity' and d['4. region'] == 'United States'), 
            data['bestMatches']))
        if len(us_equity) > 0:
            return us_equity[0]['1. symbol']
        return data['bestMatches'][0]['1. symbol']
    else:
        return None

def getSymbolYahoo(company_name, apikey=""):
    res = requests.get(
        url=YAHOO_FINANCE_URL, 
        params={
            'q': clean_company_name(company_name),
            'lang': 'en-US',
            'region': 'US',
            'quotesCount': '5',
            'newsCount': '0',
            'listsCount': '0'
        },
        headers={'User-Agent': USER_AGENT}
    )
    if res.status_code != 200:
        raise ValueError(f"Response status: {res.status_code}. {res.text}")
    try:
        data = res.json()
    except:
        return None
    
    if 'quotes' in data and len(data['quotes']) > 0:
        return data['quotes'][0]['symbol']
    else:
        return None

# def read_warn_company_names(warn_csv_path):
#     df = pd.read_csv()
#     return df['Company'].tolist()


# result = getSymbol(re.sub(r'[^\w]', ' ', "Microsoft"), API_KEY)
# print("Result ", result)