from airflow                    import DAG
from airflow.providers.docker   import DockerOperator
from airflow.utils.dates        import days_ago

from datetime                   import timedelta

default_args = {
    'owner'             : 'airflow',
    'depends_on_past'   : False,
    'email'             : ['airflow@example.com'],
    'email_on_failure'  : False,
    'email_on_retry'    : False,
    'retries'           : 1,
    'retry_delay'       : timedelta(minutes=5),
    'schedule_interval' : None,
    'start_date'        : days_ago(2),
}

dag = DAG(
    'dop_within_docker_test',
    default_args        = default_args,
    schedule_interval   = None,
    start_date          = days_ago(2),
)

dop = DockerOperator(
    api_version     = '1.37',
    docker_url      = 'TCP://docker-socket-proxy:2375',
    command         = 'echo "Successful connection from Docker container at TCP://docker-socket-proxy:2375"',
    image           = 'alpine',
    network_mode    = 'bridge',
    task_id         = 'dop_tester',
    dag             = dag,
)