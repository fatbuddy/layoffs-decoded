from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.bash import BashOperator
import boto3
import os
# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    's3_to_csv',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define the S3 bucket and prefix to load the files from
s3_bucket = 'layoffs-decoded-master'
# s3_prefix = 'path/to/my/files/'

# Define the function to get the latest folder with 'employee_csv_' in the name
def get_latest_folder():
    s3_client = boto3.client('s3')
    result = s3_client.list_objects_v2(Bucket=s3_bucket)
    folders = set()
    for obj in result.get('Contents', []):
        if obj['Key'].endswith('/'):
            folder_name = obj['Key'].split('/')[-2]
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


def list_files(bucket, prefix):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    files = s3_hook.list_keys(bucket_name=bucket, prefix=prefix)
    return files

def download_file(file_path):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    file_key = file_path
    file_name = os.path.basename(file_key)  # Extract the file name from the S3 object key
    # local_path = 'file.csv'  # Local file path to download the file to
    s3_hook.download_file(s3_bucket, file_key, file_name)
    # Move the file to the Local directory
    # local_hook.copy_to_local(local_path, local_path)
    return file_path+file_key

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

files = download_file.expand(file_path=file_paths)
csv_builder.expand(files=files)
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
# build_csv_task >> remove_tmp_dir