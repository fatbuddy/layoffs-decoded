import json

import pendulum
import datetime
import time

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash import BashOperator

from data_preparation.scraping import laid_off_employee_list
from data_preparation.scraping import scrape_employee

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    concurrency=10,
    catchup=False,
    tags=["scraping"],
)
def scrape_layoff_employee_profiles():
    """
    Scrape profiles of employee who are laid off, from https://layoffs.fyi/
    """
    @task
    def extract_layoff_links():
        """
        Extract a list of spreadsheets of laid-off employees from the main airtable sheet
        """
        employee_sheet_list = laid_off_employee_list.execute_script(saveToFile=False)
        return employee_sheet_list

    @task(
        retries=2,
        execution_timeout=datetime.timedelta(minutes=10),
    )
    def extract_employee_profiles(spreadsheet_link, output_dir):
        """
        Extract profiles of employee from a spread sheet link
        """
        print(f"{spreadsheet_link[1]} => {spreadsheet_link[4]}")
        return scrape_employee.download_employee_csv(
            list_name=spreadsheet_link[1],
            url=spreadsheet_link[4],
            output_dir=output_dir
        )
    
    @task
    def upload_employee_csv_s3(local_file_path, s3_bucket, prefix):
        """
        Upload output CSV to S3 bucket
        """
        s3_hook = S3Hook()
        file_name = local_file_path.split('/')[-1]
        s3_hook.load_file(local_file_path, f"employee_csv_{prefix}/{file_name}", s3_bucket, replace=True)

    employee_spreadsheets = extract_layoff_links()
    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )
    downloaded_csv_paths = extract_employee_profiles\
        .partial(output_dir=create_tmp_dir.output)\
        .expand(spreadsheet_link=employee_spreadsheets)
    execute_time = datetime.datetime.now().strftime("%Y%m%d")
    upload_res = upload_employee_csv_s3\
        .partial(s3_bucket='layoffs-decoded-master', prefix=execute_time)\
        .expand(local_file_path=downloaded_csv_paths)
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    )
    upload_res >> remove_tmp_dir

scrape_layoff_employee_profiles()
