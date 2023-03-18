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
def cleaning_employee_profiles_csv():
    # Define the S3 bucket and prefix to load the files from
    s3_bucket = 'layoffs-decoded-master'
    # s3_prefix = 'path/to/my/files/'

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
        keys = s3_hook.list_prefixes(bucket_name='layoffs-decoded-master')
        folders = set()
        for folder_name in keys:
            if folder_name.startswith('employee_csv_'):
                folders.add(folder_name)
        latest_folder = max(folders, default=None)
        if latest_folder is None:
            raise ValueError('No folder found with prefix employee_csv_ in the name')
        return latest_folder

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
        file_key = file_path
        file_name = os.path.basename(file_key)  # Extract the file name from the S3 object key
        # local_path = 'file.csv'  # Local file path to download the file to
        s3_hook.download_file(s3_bucket, file_key, file_name)
        # Move the file to the Local directory
        # local_hook.copy_to_local(local_path, local_path)
        return file_path+file_key

    @task
    def csv_builder(files):
        # Your csv_builder function logic here
        print("Processing File: "+files)
        pass
    # download_task = PythonOperator(
    #     task_id='download_file',
    #     python_callable=,
    #     dag=dag
    # )

    latest_folder = get_latest_folder()
    file_paths = list_files(s3_bucket, latest_folder)

    files = download_file.partial(destination=create_tmp_dir.output).expand(file_path=file_paths)
    res = csv_builder.expand(files=files)
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

cleaning_employee_profiles_csv()