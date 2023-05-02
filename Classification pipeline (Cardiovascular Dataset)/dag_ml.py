from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator as Email
from airflow.operators.python import PythonOperator 
from main import file_process


default={'owner':'Tofunmi', 'start_date': datetime(2022, 9, 9),
    'retries':'2', 'retry_delay':timedelta(seconds=5)}

ml_dag= DAG(dag_id='ml_pl', default_args=default, schedule_interval= '33 15 * * *') 

def initiate(file):
    file_process(file)

def data_finding(file2):
    file_process('cardio_base.csv').data_explore(file2)

def send_email(receivers, attachments):
    file_process('cardio_base.csv').email_opr(receivers, attachments)
    return 'Emails sent successfully'
    

start=BashOperator(task_id='process_exec', bash_command='echo "Executing Machine Learning Process"', dag=ml_dag)

task_1= PythonOperator(task_id='process_init', python_callable=initiate, \
op_kwargs={'file':'cardio_base.csv'}, dag=ml_dag)

#file_home=BashOperator(task_id='file_to_home', bash_command='mv ~/proj/clean_file.csv ~', dag=ml_dag)

task_2 = PythonOperator(task_id='data_exploration', python_callable=data_finding, op_kwargs={'file2':'clean_file.csv'}, dag=ml_dag)

email_task = PythonOperator(task_id='email_notification', python_callable=send_email, op_kwargs={'receivers':['johncaul@yahoo.com'], 'attachments':['explor_info.txt']}, dag=ml_dag)

start >> task_1 >> task_2 >> email_task