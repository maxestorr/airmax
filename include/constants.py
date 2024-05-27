import os

from airflow.configuration import AIRFLOW_HOME
from airflow.datasets import Dataset
from dotenv import load_dotenv


load_dotenv()

MINIO_URI=os.getenv("MINIO_URI")
MINIO_USER=os.getenv("MINIO_USER")
MINIO_PASSWORD=os.getenv("MINIO_PASSWORD")
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

MY_FILE=Dataset(f"{AIRFLOW_HOME}/test.csv")
