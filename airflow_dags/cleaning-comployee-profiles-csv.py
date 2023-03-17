from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.amazon.aws.operators.s3_to_local import S3ToLocalOperator
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
s3_bucket = 'my-s3-bucket'
s3_prefix = 'employee_csv_'

# Create a boto3 S3 client object
s3 = boto3.client('s3')

# Get the latest datetime for the prefix
s3_prefix_list = [o['Prefix'] for o in client.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)['CommonPrefixes']]
latest_s3_prefix = sorted(s3_prefix_list)[-1]

# Add datetime to prefix and define S3 prefix for S3ListOperator and S3ToLocalOperator
datetime_str = datetime.now().strftime("%Y%m%d")
s3_prefix_with_datetime = latest_s3_prefix + datetime_str + '/'

# Define the S3ListOperator to list the files in the S3 bucket
list_files_task = S3ListOperator(
    task_id='list_files',
    bucket=s3_bucket,
    prefix=s3_prefix_with_datetime,
    dag=dag
)

# Define the S3ToLocalOperator to download the files to the local machine
download_files_task = S3ToLocalOperator(
    task_id='download_files',
    bucket=s3_bucket,
    prefix=s3_prefix_with_datetime,
    local_directory='/path/to/local/folder/',
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

# Set task dependencies
list_files_task >> download_files_task >> build_csv_task