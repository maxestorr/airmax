"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

import os

from airflow.decorators import dag, task
from pendulum import datetime
from hubspot import HubSpot
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
import pandas as pd


load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
MINIO_URI=os.getenv("MINIO_URI")
MINIO_USER=os.getenv("MINIO_USER")
MINIO_PASSWORD=os.getenv("MINIO_PASSWORD")

hubspot_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
)
def hubspot_pipeline():
    @task()
    def get_deals():
        deals = hubspot_client.crm.deals.get_all()
        deals = pd.DataFrame([deal.to_dict()['properties'] for deal in deals])

        return deals


    def save_deals(deals):
        minio_client = Minio(
            MINIO_URI,
            MINIO_USER,
            MINIO_PASSWORD
        )
        bucket_name = "my-bucket"
        destination_file = "hubspot_deals.csv"
        found = minio_client.bucket_exists(bucket_name)
        if not found:
            minio_client.make_bucket(bucket_name)
            print(f"Created bucket {bucket_name}")
        else:
            print(f"Bucket {bucket_name} already exists")
        
        try:
            minio_client.fput_object(
                bucket_name, destination_file, deals.to_csv()
            )
        except S3Error as error:
            print(f"Error occured: {error}")

    deals = get_deals()
    save_deals(deals)

hubspot_pipeline()
