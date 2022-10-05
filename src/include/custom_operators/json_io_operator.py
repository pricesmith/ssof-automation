"""
Supply JSON input into the Docker Container

Extract file outputs (XLSX, CSV, etc) from within the Docker Container

Operate on multi-worker Airflow deployments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
EXAMPLE USAGE:
# from airflow import DAG
# from airflow.operators import PythonOperator
# from include.custom_operators.json_io_operator import JsonIoOperator

# dag = DAG(...)

# input_task_id = ‘python_task’

# input_task = PythonOperator(
#     task_id = input_task_id,
#     …,
# )

# dockerTask = JsonIoOperator(
#     docker_url            = ’unix:///var/run/docker.sock’,
#     image                 = ...,
#     volumes               = ...,
#     environment           = ...,
#     task_id               = ’docker_task’,
#     dag                   = dag,
#     output_dir_path       = ...,          # location within container to which your output will be written
#     shared_dir_path       = ...,          # your NFS dir or S3 location
#     input_task_id         = input_task_id,
# )
"""
import os
import json
import tempfile

from airflow.operators import DockerOperator

# Inherit functionality from DockerOperator --
# The DockerOperator takes care of supplying arguments necessary 
# to run the container and starts up the container.
class JsonIoOperator(DockerOperator):

    def __init__(
        self, 
        input_task_id, 
        shared_dir_path,
        output_dir_path = 'tmp/output',
        *args, 
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.input_task_id      = input_task_id
        self.shared_dir_path    = shared_dir_path
        self.output_dir_path    = output_dir_path
        
    def execute_to_temp_nfs(self, context):
        # pass input logic goes here
        input = self.xcom_pull(task_ids = self.input_task_id, context = context)
        self.environment['CONTAINER_INPUT'] = json.dumps(input)

        # setup output logic goes here
        self.environment['OUTPUT_DIR'] = self.output_dir_path
        tmp_dir = tempfile.TemporaryDirectory(dir=self.shared_dir_path)
        tmp_dir_path = tmp_dir.name
        
        # append volume
        volume = "{}:{}:rw".format(tmp_dir_path, self.output_dir_path)
        self.volumes.append(volume)

        # run the container
        super().execute(context)

        # load output into Airflow logic goes here

        # returns output file path
        return tmp_dir_path

    def execute_to_xcom(self, context):
        # pass input logic goes here
        input = self.xcom_pull(task_ids     = self.input_task_id, context = context)
        self.environment['CONTAINER_INPUT'] = json.dumps(input)

        # setup output logic goes here
        self.environment['OUTPUT_DIR'] = self.output_dir_path
        tmp_dir = tempfile.TemporaryDirectory(dir = self.shared_dir_path)
        files = {}

        # using context to avoid explicit garbage collection code
        with tmp_dir as tmp_dir:
            tmp_dir_path = tmp_dir.name

            # append volume
            volume = "{}:{}:rw".format(tmp_dir_path, self.output_dir)
            self.volumes.append(volume)

            # run the container
            super().execute(context)

            # load output into Airflow logic goes here

            # extract files
            for filename in os.listdir(tmp_dir_path):
                filepath = os.path.join(tmp_dir_path, filename)
                with open(filepath, 'rb') as f:
                    files[filename] = f.read()

        # returns files
        return files
