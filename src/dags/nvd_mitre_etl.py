import os
import json
from os                 import getenv
from datetime           import datetime
from airflow            import DAG
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from workflows.http     import nvd_client

DAG_ID          = os.path.basename(__file__).replace('.pyc', '').replace('py', '')
DAG_OWNER_NAME  = 'airflow'
USER_EMAIL      = 'psmith.code@gmail.com'
DOCKER_IMAGE    = ''
DEBUG           = getenv('DEBUG', False)
LOG_LEVEL       = getenv('LOG_LEVEL', 'info')

def _extract_vulns():
    vulns_string = '{vuln1, vuln2, vuln3m, vuln4, vuln5}'
    order_vulns_dict = json.loads(vulns_string)
    return order_vulns_dict

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
def update_nvd_vulns_etl():
    """
    ### NVD ETL Process Documentation

    """

    @task('extract_vulnerabilities', retries = 2)
    def extract():


        """
        In RDF, you have "Entities (Nodes) and Properties (Edges).

        When we extract data that we intend to map into RDF Triples, 
        we are also extracting what will eventually be mapped into these 
        RDF 'Resources' (Resource is the encapsulating term for both Entities and Triples).
        """
        # nvd.get_all_vulnerabilities()
        # nvd.get_all_products()
        # mitre.get_all_resources() -- # Not to be confused with RDF Resources
        pass

    @task()
    def transform():
        # rdf.map_to_triples()
        pass

    @task()
    def load():
        """
        In this case, we'll load the data in parallel-
            - the original data to a Postgres database,
            - and the newly formed triples to a triplestore!
        """
        pass
