import io
import pandas as pd
import requests
import csv
from random import randint
from time import sleep


FMP_API_ENDPOINT="https://financialmodelingprep.com/api"
FMP_API_KEY=""

def process_fmp_financial_statements(file_path):
    raw_df = pd.read_csv(file_path)
    raw_df.rename({"Unnamed: 1": "metric"}, axis=1, inplace=True)
    df = raw_df[~raw_df['metric'].isna()]
    df = df.drop("date", axis=1)
    df = df.rename({"metric": "date"}, axis=1)
    df = df.set_index("date").transpose()
    df = df.sort_index(ascending=False)
    return df


def pull_fmp_financial_statements(stock_symbols, output_dir, api_key):
    statment_types = ["income-statement", "balance-sheet-statement", "cash-flow-statement"]
    session = requests.Session()
    output_files = []
    for raw_sym in stock_symbols:
        sym = raw_sym.replace("/", "-")
        for stmt_type in statment_types:
            statement_url = f"{FMP_API_ENDPOINT}/v3/{stmt_type}/{sym}"
            resp = session.get(url = statement_url, params={
                    "apikey": api_key,
                    "period": "quarter",
                    "limit": 1,
                    "datatype": "csv"
                })
            if resp.status_code != 200:
                print(f"error in pulling data {statement_url}")
                raise RuntimeError(f"http status is {resp.status_code}")
            file_name = f"{output_dir}/{sym}-{stmt_type}"
            raw_file_path = f"{file_name}-raw.csv"
            processed_file_path = f"{file_name}.csv"
            with open(raw_file_path, 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                reader = csv.reader(resp.content.decode('utf-8').splitlines())
                for row in reader:
                    if len(row) >= 3 and len(row[2]) > 0:
                        writer.writerow(row)
            df = process_fmp_financial_statements(raw_file_path)
            df.to_csv(processed_file_path)
            output_files.append(processed_file_path)
            sleep(randint(1,3))
    return output_files
