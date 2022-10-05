import os
import logging

from os                 import getenv, path
from datetime           import datetime, timedelta
from sys import api_version

from airflow            import DAG
from airflow.decorators import dag, task
from airflow.operators  import PythonOperator, BranchPythonOperator, BashOperator, DockerOperator

#########################
#                       #
#########################
DAG_ID          = os.path.basename(__file__).replace('.pyc', '').replace('py', '')
DAG_OWNER_NAME  = 'airflow'
USER_EMAIL      = 'psmith.code@gmail.com'
DOCKER_IMAGE    = 'bde2020/spark-master:latest'
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

def is_repo_cloned():
    if os.path.exists('home/airflow/spark_job.py'):
        return 'dummy'
    return 'git_clone'

with DAG(DAG_ID, default_args=default_args) as dag:

    t_git_clone = BashOperator(
        task_id         = 'git_clone',
        bash_command    = 'git_clone http://github.com/pricesmith/spark_job.py',
    )

    t_git_pull = BashOperator(
        task_id         = 'git_pull',
        bash_command    = 'cd /home/airflow/spark_jobs && git pull',
        trigger_rule    = 'one_success',
    )

    t_check_repo = BranchPythonOperator(
        task_id         = 'if_repo_exists',
        python_callable = is_repo_cloned,
    )

    t_check_repo    >> t_git_clone
    t_check_repo    >> t_dummy >> t_git_pull
    t_git_clone     >> t_git_pull

    t_docker = DockerOperator(
        task_id         = 'docker_cmd',
        image           = DOCKER_IMAGE,
        api_version     = 'auto',
        auto_remove     = True,
        volumes         = ['home/airflow/spark_job:/spark_job'],
        command         = '/spark/bin/spark-submit --master local[*] /spark_job/spark_job.py',
        docker_url      = 'unix://var/run/docker.sock',
        network_mode    = 'bridge',
        environment     = {
            'PYSPARK_PYTHON'    : 'python3',
            'SPARK_HOME'        : '/spark'
        },
    )

    t_git_pull      >> t_docker

