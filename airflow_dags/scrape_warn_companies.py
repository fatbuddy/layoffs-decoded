import json

import pendulum
import pandas as pd
import uuid

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash import BashOperator

from data_preparation.scraping import scrape_warn
from data_preparation.scraping import scrape_employee_gsheet

ALPHA_VANTAGE_API_KEY='DEO388ZM3UEZ34M8'
WARN_COLUMNS = ['State', 'Company', 'City', 'Number of Workers', 'WARN Received Date',
       'Effective Date', 'Closure/Layoff', 'Temporary/Permanent', 'Union',
       'Region', 'County', 'Industry', 'Notes']
SYMBOL_BATCH_SIZE=1000

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["scraping"],
)
def scrape_warn_companies():
    def chunks(l, n):
        """Yield n number of striped chunks from l."""
        for i in range(0, n):
            yield l[i::n]

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
        # return [0]
        # company_names = company_data_df['Company'].tolist()
        # company_data_df.fillna('', inplace=True)
        # company_data = company_data_df.to_records(index=False).tolist()
        # print(company_names)
        # return [company_names[:20], company_names[20:40]]
        # return list(chunks(company_names, 100))
    
    @task
    def retrieve_company_symbol(start_idx, batch_size, api_key, output_dir):
        print(start_idx)
        companies_with_symbol = []
        company_data_df = pd.read_csv(f"{output_dir}/warn.csv", encoding='utf-8')
        company_batch = company_data_df.iloc[start_idx:(start_idx+batch_size)].to_records(index=False).tolist()
        # company_names = company_data_df.iloc[start_idx:(start_idx+batch_size)]['Company'].tolist()
        # columns = WARN_COLUMNS + ['Symbol']
        # print(start_idx)
        # company_symbols = []
        for c in company_batch:
            c_arr = list(c)
            s = scrape_warn.getSymbol(c_arr[1], api_key)
            if s is not None:
                c_arr.append(s)
                companies_with_symbol.append(c_arr)
            # company_symbols.append(scrape_warn.getSymbol(c[1], api_key))
        # companies_with_symbol = list(filter(
        #     lambda cs: cs[1] is not None, 
        #     zip(company_batch, company_symbols)
        # ))
        if len(companies_with_symbol) > 0:
            path = f"{output_dir}/company_symbol_{''.join(str(uuid.uuid4()).split('-'))}.csv"
            pd.DataFrame\
                .from_records(companies_with_symbol, columns=(WARN_COLUMNS+['Symbol']))\
                .to_csv(path, header=True, index=False)
            return path
        return None
    
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
    # remove_tmp_dir = BashOperator(
    #     task_id="remove_tmp_dir",
    #     bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    # )
    # get_symbol_res >> remove_tmp_dir
    
scrape_warn_companies()
    # @task
    # def extract_employee_profiles(spreadsheet_link, output_dir):
    #     """
    #     Extract profiles of employee from a spread sheet link
    #     """
    #     print(f"{spreadsheet_link[1]} => {spreadsheet_link[4]}")
    #     return scrape_employee.download_employee_csv(
    #         list_name=spreadsheet_link[1],
    #         url=spreadsheet_link[4],
    #         output_dir=output_dir
    #     )
    
    # @task
    # def upload_employee_csv_s3(local_file_path, s3_bucket):
    #     """
    #     Upload output CSV to S3 bucket
    #     """
    #     s3_hook = S3Hook()
    #     file_name = local_file_path.split('/')[-1]
    #     s3_hook.load_file(local_file_path, f"employees/{file_name}", s3_bucket, replace=True)

    # employee_spreadsheets = extract_layoff_links()
    # create_tmp_dir = BashOperator(
    #     task_id="create_tmp_dir",
    #     bash_command="mktemp -d 2>/dev/null"
    # )
    # downloaded_csv_paths = extract_employee_profiles\
    #     .partial(output_dir=create_tmp_dir.output)\
    #     .expand(spreadsheet_link=employee_spreadsheets)
    # upload_res = upload_employee_csv_s3\
    #     .partial(s3_bucket='layoffs-decoded-master')\
    #     .expand(local_file_path=downloaded_csv_paths)
    # remove_tmp_dir = BashOperator(
    #     task_id="remove_tmp_dir",
    #     bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    # )
    # upload_res >> remove_tmp_dir

# scrape_layoff_employee_profiles()
