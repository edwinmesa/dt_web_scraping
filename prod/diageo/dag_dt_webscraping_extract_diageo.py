# import libraries
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator
from airflow.utils.trigger_rule import TriggerRule

# define the default_args

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'email': 'edwinsar.mes@gmail.com',
    'email_on_failure': True,
    'email_on_retry': True,
    'retry_delay': timedelta(minutes=2),
}

# programmer specific settings

dag_python = DAG(
    dag_id="dag_dt_webscraping_extract_diageo_v20",
    default_args=default_args,
    schedule_interval='03 05 * * *',
#    dagrun_timeout=timedelta(minutes=5),
    description='extract data scraping for diageo',
    start_date=airflow.utils.dates.days_ago(1)
    )

# execute the command

# success_email_body = f"""Hi, <br><br>process_incoming_files DAG has been failed successfully now."""

t1 = BashOperator(
    task_id='webscraping_extract_diageo',
    bash_command='/home/pydev/pyenv/venv1/bin/python3 /home/pydev/workflow/dt_web_scraping/prod/diageo/web_scraping_diageo_v1.py',
    dag=dag_python)

# t1Failed = EmailOperator(
#     dag=dag_python,
#     trigger_rule=TriggerRule.ONE_FAILED,
#     task_id='task Diageo Failed',
#     to='edwin.mesa@dislicores.com',
#     subject='task Diageo Failed',
#     html_content='The diageo has failed'
# )


# send_mail = EmailOperator(
#     task_id="send_mail", 
#     to='edwinsar.mes@gmail.com',
#     subject='Airflow Success: process_incoming_files',
#     html_content=success_email_body,
#     dag=dag_python)

# t1

# send_mail.set_upstream(t1)