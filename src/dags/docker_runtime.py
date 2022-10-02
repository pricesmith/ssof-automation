import os
import logging
from os                 import getenv
from datetime           import datetime, timedelta
from airflow            import DAG
from airflow.decorators import dag, task
from airflow.operators  import PythonOperator, BashOperator, DockerOperator

#########################
#                       #
#########################
DAG_ID          = os.path.basename(__file__).replace('.pyc', '').replace('py', '')
DAG_OWNER_NAME  = 'airflow'
USER_EMAIL      = 'psmith.code@gmail.com'
DOCKER_IMAGE    = ''
DEBUG           = getenv('DEBUG', False)
LOG_LEVEL       = getenv('LOG_LEVEL', 'info')

default_args = {
    'owner'             : DAG_OWNER_NAME,
    'description'       : 'Extract and Transform NVD Data',
    'depend_on_past'    : False,
    'start_date'        : datetime(2022, 1, 1),
    'schedule_interval' : "5 * * * *",
    'email_on_failure'  : True,
    'email'             : USER_EMAIL,
    'retries'           : 0,
    'force_pull'        : True,
    'catchup'           : False,
}

@dag(DAG_ID, default_args=default_args)
def taskflow():
    