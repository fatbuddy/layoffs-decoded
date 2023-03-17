from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.amazon.aws.operators.s3_to_local import S3ToLocalOperator
from airflow.operators.bash import BashOperator
import boto3
# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
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
latest_folder = get_latest_folder()

# Define the S3ListOperator to list the files in the S3 bucket
list_files_task = S3ListOperator(
    task_id='list_files',
    bucket=s3_bucket,
    prefix=f'{latest_folder}',
    dag=dag
)

# Define the S3ToLocalOperator to download the files to the local machine
download_files_task = S3ToLocalOperator(
    task_id='download_files',
    bucket=s3_bucket,
    prefix=f'{latest_folder}',
    local_directory=create_tmp_dir.output,
    dag=dag
)

# Define the PythonOperator to call the csv_builder function
def csv_builder(ds, **kwargs):
    # Your csv_builder function logic here
    pass

build_csv_task = PythonOperator(
    task_id='build_csv',
    python_callable=csv_builder,
    provide_context=True,
    dag=dag
)
remove_tmp_dir = BashOperator(
    task_id="remove_tmp_dir",
    bash_command="rm -rf {{ ti.xcom_pull(task_ids='create_tmp_dir') }}"
)

# Set task dependencies
list_files_task >> download_files_task >> build_csv_task >> remove_tmp_dir