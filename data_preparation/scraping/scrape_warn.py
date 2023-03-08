import requests 
import pandas as pd
import time
import re

API_KEY = "DEO388ZM3UEZ34M8"

def getSymbol(company_name, apikey):
    url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + company_name + "&apikey=" + apikey
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

    res = requests.get(url=url, headers={'User-Agent': user_agent})
    try :
        data = res.json()
    except:
        return None
        
    if 'bestMatches' in data and len(data['bestMatches']) > 0:
        return data['bestMatches'][0]['1. symbol']
    else:
        return None

def warn_company_data(warn_csv_path):
    df = pd.read_csv(warn_csv_path)
    return df.to_records().tolist()


# result = getSymbol(re.sub(r'[^\w]', ' ', "Microsoft"), API_KEY)
# print("Result ", result)