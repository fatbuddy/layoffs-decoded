from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator
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
    #     s3_client = boto3.client(
    #     's3',
    #     aws_access_key_id=os.environ.get('ACCESS_KEY'),
    #     aws_secret_access_key=os.environ.get('SECRET_KEY'),
    #     aws_session_token=os.environ.get('SESSION_TOKEN')
    # )
    #     result = s3_client.list_objects_v2(Bucket=s3_bucket)
        s3_hook = S3Hook()
        keys = s3_hook.list_keys(
            bucket_name='layoffs-decoded-master',
            prefix="employee_csv_",
            page_size=200
        )
        sorted_keys = sorted(keys, reverse=True)
        latest_dir = sorted_keys[0].split("/")[0]
        return latest_dir
        # print(keys)
        # folders = set()
        # for folder_name in keys:
        #     if folder_name.startswith('employee_csv_'):
        #         folders.add(folder_name)
        # latest_folder = max(folders, default=None)
        # if latest_folder is None:
        #     raise ValueError('No folder found with prefix employee_csv_ in the name')
        # return latest_folder

    create_tmp_dir = BashOperator(
        task_id="create_tmp_dir",
        bash_command="mktemp -d 2>/dev/null"
    )

    # Get the latest folder with 'employee_csv_' in the name

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
        # Your csv_builder function logic here
        print("Processing File: "+file)
    # download_task = PythonOperator(
    #     task_id='download_file',
    #     python_callable=,
    #     dag=dag
    # )

    latest_folder = get_latest_folder()
    file_paths = list_files(s3_bucket, latest_folder)
    files = download_file.partial(destination=create_tmp_dir.output).expand(file_path=file_paths)
    res = clean_employee_csv.expand(file=files)
    # Define the PythonOperator to call the csv_builder function


    # build_csv_task = PythonOperator(
    #     task_id='build_csv',
    #     python_callable=csv_builder,
    #     provide_context=True,
    #     dag=dag
    # )
    remove_tmp_dir = BashOperator(
        task_id="remove_tmp_dir",
        bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
    )

    # # Set task dependencies
    res >> remove_tmp_dir

clean_employee_profiles_csv()