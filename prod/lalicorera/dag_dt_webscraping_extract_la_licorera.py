# import libraries
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

# define the default_args

default_args = {
    'owner': 'airflow',
    'retry_delay': timedelta(minutes=2),
}

# programmer specific settings

dag_python = DAG(
    dag_id="dag_dt_webscraping_extract_la_licorera_v4",
    default_args=default_args,
    schedule_interval='00 08 * * *',
#    dagrun_timeout=timedelta(minutes=5),
    description='extract data scraping for la licorera',
    start_date=airflow.utils.dates.days_ago(1)
    )

# execute the command

t1 = BashOperator(
    task_id='webscraping_extract_la_licorera',
    bash_command='/home/edwsar/pyenv/venv3/bin/python3 /home/edwsar/workflow/dt_web_scraping/prod/lalicorera/web_scraping_la_licorera_v2.py',
    dag=dag_python)

