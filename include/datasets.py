import os

from airflow.configuration import AIRFLOW_HOME
from airflow.datasets import Dataset
from minio import Minio
from dotenv import load_dotenv


load_dotenv()

MINIO_URI=os.getenv("MINIO_URI")
MINIO_USER=os.getenv("MINIO_USER")
MINIO_PASSWORD=os.getenv("MINIO_PASSWORD")

minio_client = Minio(
    MINIO_URI,
    MINIO_USER,
    MINIO_PASSWORD
)

MY_FILE=Dataset(f"{AIRFLOW_HOME}/test.csv")
