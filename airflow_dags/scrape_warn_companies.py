import json

import pendulum
import pandas as pd
import uuid
import datetime
import time

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.operators.bash import BashOperator

from data_preparation.scraping import scrape_warn
from data_preparation.scraping import scrape_employee_gsheet

ALPHA_VANTAGE_API_KEY='DEO388ZM3UEZ34M8'
WARN_COLUMNS = ['State', 'Company', 'City', 'Number of Workers', 'WARN Received Date',
       'Effective Date', 'Closure/Layoff', 'Temporary/Permanent', 'Union',
       'Region', 'County', 'Industry', 'Notes']
SYMBOL_BATCH_SIZE=100

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["scraping"],
)
def scrape_warn_companies():
    """
    Scrape company data from WARN at https://layoffdata.com/data/
    """
    @task
    def download_company_list_csv(output_dir):
        """
        Extract a list of companies from WARN spreadsheet
        https://docs.google.com/spreadsheets/d/1GWMWe33pWRUxCmdXLrl7X2-BvG5ePKOovNQXBqgGC14/edit#gid=0
        """
        warn_csv_path = scrape_employee_gsheet.download_gsheet_csv(
            "warn", 
            "https://docs.google.com/spreadsheets/d/1GWMWe33pWRUxCmdXLrl7X2-BvG5ePKOovNQXBqgGC14/edit#gid=0",
            output_dir
        )
        company_data_df = pd.read_csv(warn_csv_path, encoding='utf-8')
        company_count = company_data_df.shape[0]
        idx_range = list(range(0, company_count, SYMBOL_BATCH_SIZE))
        return idx_range
        # return [0, 50]
    
    @task(
        retries=2,
        execution_timeout=datetime.timedelta(minutes=10),
    )
    def retrieve_company_symbol(start_idx, batch_size, api_key, output_dir):
        print(start_idx)
        companies_with_symbol = []
        company_data_df = pd.read_csv(f"{output_dir}/warn.csv", encoding='utf-8')
        end_idx = start_idx+batch_size
        if company_data_df.shape[0] < end_idx:
            end_idx = company_data_df.shape[0]
        company_batch = company_data_df.iloc[start_idx:end_idx].to_records(index=False).tolist()
        for c in company_batch:
            c_arr = list(c)
            s = scrape_warn.getSymbol(c_arr[1], api_key)
            if s is not None:
                print(f"{c_arr[1]} = {s}")
                c_arr.append(s)
                companies_with_symbol.append(c_arr)
        if len(companies_with_symbol) > 0:
            path = f"{output_dir}/company_symbol_{''.join(str(uuid.uuid4()).split('-'))}.csv"
            pd.DataFrame\
                .from_records(companies_with_symbol, columns=(WARN_COLUMNS+['Symbol']))\
                .to_csv(path, header=True, index=False)
            return path
        return None
    
    @task
    def merge_company_symbol_csv(csv_list, output_dir):
        df = None
        final_csv_path = f"{output_dir}/warn_symbol.csv"
        for csv_path in csv_list:
            if df is None:
                df = pd.read_csv(csv_path)
            else:
                next_df = pd.read_csv(csv_path)
                df = pd.concat([df, next_df], axis=0, ignore_index=True)
        df.to_csv(final_csv_path, header=True, index=False)
        return final_csv_path
    
    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )
    company_name_res = download_company_list_csv(output_dir=create_tmp_dir.output)
    get_symbol_res = retrieve_company_symbol\
        .partial(
            batch_size=SYMBOL_BATCH_SIZE,
            api_key=ALPHA_VANTAGE_API_KEY, 
            output_dir=create_tmp_dir.output
        )\
        .expand(start_idx=company_name_res)
    merge_res = merge_company_symbol_csv(
        csv_list=get_symbol_res, 
        output_dir=create_tmp_dir.output)
    upload_res = LocalFilesystemToS3Operator(
        task_id="upload_company_symbol_csv",
        filename=merge_res,
        dest_key=f"warn_symbol_{int(time.time())}.csv",
        dest_bucket="layoffs-decoded-master",
        replace=True
    )
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    )
    upload_res >> remove_tmp_dir
    
scrape_warn_companies()
