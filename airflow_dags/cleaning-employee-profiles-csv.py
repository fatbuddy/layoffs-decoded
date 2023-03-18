from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash import BashOperator
import os
import pendulum

# Define the DAG
@dag(
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    concurrency=10,
    schedule_interval='@daily',
    tags=["cleaning"],
    catchup=False
)
def clean_employee_profiles_csv():
    s3_bucket = 'layoffs-decoded-master'

    # Define the function to get the latest folder with 'employee_csv_' in the name
    @task
    def get_latest_folder():
        s3_hook = S3Hook()
        keys = s3_hook.list_keys(
            bucket_name=s3_bucket,
            prefix="employee_csv_",
            page_size=200
        )
        sorted_keys = sorted(keys, reverse=True)
        latest_dir = sorted_keys[0].split("/")[0]
        return latest_dir

    @task
    def list_files(bucket, prefix):
        s3_hook = S3Hook()
        files = s3_hook.list_keys(bucket_name=bucket, prefix=prefix)
        return files

    @task
    def download_file(file_path, destination):
        s3_hook = S3Hook()
        file_name = file_path.split("/")[-1]
        local_path = f"{destination}/{file_name}"
        s3_hook.download_file(
            key=file_path, 
            bucket_name=s3_bucket, 
            local_path=local_path,
            preserve_file_name=True)
        return local_path

    @task
    def clean_employee_csv(file):
        print("Processing File: "+file)

    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )
    latest_folder = get_latest_folder()
    file_paths = list_files(s3_bucket, latest_folder)
    files = download_file\
        .partial(destination=create_tmp_dir.output)\
        .expand(file_path=file_paths)
    res = clean_employee_csv.expand(files=files)
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    )
    res >> remove_tmp_dir

clean_employee_profiles_csv()