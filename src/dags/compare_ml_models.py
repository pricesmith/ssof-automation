import os
import logging

from os                 import getenv
from datetime           import datetime, timedelta
from random             import randint

from airflow            import DAG
from airflow.decorators import dag, task
from airflow.operators  import PythonOperator, BranchPythonOperator, BashOperator

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
    'email_on_failure'  : True,
    'email'             : USER_EMAIL,
    'retries'           : 0,
    'force_pull'        : True,
}

def _determine_best_model(ti):
    scores = ti.xcom_pull(task_ids = [
        't_model_A',
        't_model_B',
        't_model_C',
    ])

    highest_score = max(scores)
    if (highest_score > 80):
        return 'is_accurate'
    return 'is_innaccurate'

def _t_model():
    return randint(1, 100)

with DAG(DAG_ID, default_args=default_args) as dag:

    t_model_A = PythonOperator(
        task_id         = 't_model_A',
        python_callable = _t_model,
    )

    t_model_B = PythonOperator(
        task_id         = 'training_model_A',
        python_callable = _t_model,
    )

    t_model_C = PythonOperator(
        task_id         = 't_model_A',
        python_callable = _t_model,
    )

    determine_best_model = BranchPythonOperator(
        task_id         = 'determine_best_model',
        python_callable = _determine_best_model,
    )

    is_accurate = BashOperator(
        task_id         = 'is_accurate',
        bash_command    = 'echo accurate',
    )

    is_inaccurate = BashOperator(
        task_id         = 'is_inaccurate',
        bash_command    = 'echo inaccurate',
    )

    [t_model_A, t_model_B, t_model_C] >> determine_best_model >> [is_accurate, is_inaccurate]
