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
from airflow.models import Variable

from data_preparation.scraping import scrape_financials_fmp

WARN_COLUMNS = ['State', 'Company', 'City', 'Number of Workers', 'WARN Received Date',
       'Effective Date', 'Closure/Layoff', 'Temporary/Permanent', 'Union',
       'Region', 'County', 'Industry', 'Notes']

@dag(
    schedule_interval='@daily',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["scraping"],
    concurrency=10,
    max_active_runs=1,
)
def scrape_company_financials():
    """
    Scrape company financial data from FMP at https://site.financialmodelingprep.com/developer/docs
    """
    @task(
        retries=2,
        execution_timeout=datetime.timedelta(minutes=3),
        retry_delay=datetime.timedelta(minutes=2),
    )
    def pull_company_financial_data(symbols, output_dir):
        """
        TODO DOC
        """
        api_key = Variable.get("FMP_API_KEY", default_var="")
        outputs = scrape_financials_fmp.pull_fmp_financial_statements(symbols, output_dir, api_key)
        return outputs
    
    @task(
        retries=2,
        execution_timeout=datetime.timedelta(minutes=1),
        retry_delay=datetime.timedelta(minutes=1),
    )
    def retrieve_company_symbols():
        return [["GOOGL", "AAPL", "MSFT"]]
    
    @task(
        retries=2,
        execution_timeout=datetime.timedelta(minutes=3),
        retry_delay=datetime.timedelta(minutes=1),
    )
    def upload_fmp_csv_s3(local_file_paths, s3_bucket, prefix):
        """
        Upload output CSV to S3 bucket
        """
        s3_hook = S3Hook()
        for fp in local_file_paths:
            file_name = fp.split('/')[-1]
            s3_hook.load_file(fp, f"company_financials_{prefix}/{file_name}", s3_bucket, replace=True)
    
    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )
    company_symbol_list = retrieve_company_symbols()
    company_financial_csv_paths = pull_company_financial_data\
        .partial(output_dir=create_tmp_dir.output)\
        .expand(symbols=company_symbol_list)
    execute_time = datetime.datetime.now().strftime("%Y%m%d")
    upload_res = upload_fmp_csv_s3\
        .partial(s3_bucket='layoffs-decoded-master', prefix=execute_time)\
        .expand(local_file_paths=company_financial_csv_paths)
    
    # company_name_res = download_company_list_csv(output_dir=create_tmp_dir.output)
    # get_symbol_res = retrieve_company_symbol\
    #     .partial(output_dir=create_tmp_dir.output)\
    #     .expand(start_idx=company_name_res)
    # merge_res = merge_company_symbol_csv(
    #     csv_list=get_symbol_res, 
    #     output_dir=create_tmp_dir.output)
    # upload_res = LocalFilesystemToS3Operator(
    #     task_id="upload_company_symbol_csv",
    #     filename=merge_res,
    #     dest_key=f"warn_symbol_{int(time.time())}.csv",
    #     dest_bucket="layoffs-decoded-master",
    #     replace=True
    # )
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    )
    upload_res >> remove_tmp_dir
    
scrape_company_financials()
