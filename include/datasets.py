from airflow.configuration import AIRFLOW_HOME
from airflow.datasets import Dataset


MY_FILE=Dataset(f"{AIRFLOW_HOME}/test.csv")
