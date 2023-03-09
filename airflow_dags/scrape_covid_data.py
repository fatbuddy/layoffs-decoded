from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import requests


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 9),
    'retries': 1
}

dag = DAG(
    'download_and_filter_covid_data',
    default_args=default_args,
    schedule_interval='@daily'
)

def download_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    response = requests.get(url)
    
    with open("owid-covid-data.csv", "wb") as f:
        f.write(response.content)
        
def filter_data():
    covid_df = pd.read_csv('owid-covid-data.csv')
    US_covid_df = covid_df[covid_df['location']=='United States']
    US_covid_df = US_covid_df.dropna(subset=["total_cases"])
    US_covid_df.to_csv('us-covid-data.csv', index=False)

download_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag
)

filter_task = PythonOperator(
    task_id='filter_data',
    python_callable=filter_data,
    dag=dag
)

download_task >> filter_task
