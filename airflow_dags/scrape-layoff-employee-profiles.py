import json

import pendulum

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash import BashOperator

from data_preparation.scraping import laid_off_employee_list
from data_preparation.scraping import scrape_employee_gsheet


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
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
        return employee_sheet_list[:5]

    @task
    def extract_employee_profiles(spreadsheet_link, output_dir):
        """
        Extrack profiles of employee from a spreadsheet link
        """
        print(f"{spreadsheet_link[1]} => {spreadsheet_link[4]}")
        return scrape_employee_gsheet.download_gsheet_csv(
            list_name=spreadsheet_link[1],
            url=spreadsheet_link[4],
            output_dir=output_dir
        )
    
    @task
    def upload_employee_csv_s3(local_file_path, s3_bucket):
        s3_hook = S3Hook()
        file_name = local_file_path.split('/')[-1]
        s3_hook.load_file(local_file_path, f"employees/{file_name}", s3_bucket, replace=True)

    employee_spreadsheets = extract_layoff_links()
    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )
    downloaded_csv_paths = extract_employee_profiles\
        .partial(output_dir=create_tmp_dir.output)\
        .expand(spreadsheet_link=employee_spreadsheets)
    upload_res = upload_employee_csv_s3\
        .partial(s3_bucket='layoffs-decoded-master')\
        .expand(local_file_path=downloaded_csv_paths)
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
        
    )
    upload_res >> remove_tmp_dir

scrape_layoff_employee_profiles()