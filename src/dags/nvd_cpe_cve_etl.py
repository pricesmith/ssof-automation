import os
import airflow
from os                 import getenv
from datetime           import datetime
from airflow            import DAG
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator

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
    'email_on_failure'  : True,
    'email'             : USER_EMAIL,
    'retries'           : 0,
    'force_pull'        : True,
}

@dag(
    DAG_ID, 
    default_args        = default_args, 
    schedule_interval   ='@daily', 
    catchup             = False,
    tags = ['NVD, Vulnerabilities', 'Products']
)
def nvd_etl():
    """
    ### NVD ETL Process Documentation

    """

    @task()
    def extract():
        pass

    @task()
    def transform():
        pass

    @task()
    def load():
        pass
