"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

from airflow.decorators import dag, task
from pendulum import datetime
from hubspot import HubSpot
from minio import Minio
from minio.error import S3Error
import pandas as pd

from include.constants import (
    HUBSPOT_ACCESS_TOKEN,
    MY_FILE
)


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
    def get_deals() -> pd.DataFrame:
        deals = hubspot_client.crm.deals.get_all()
        deals = pd.DataFrame([deal.to_dict()['properties'] for deal in deals])

        return deals

    @task
    def save_deals(deals: pd.DataFrame):
        deals.to_csv(MY_FILE)

    save_deals(get_deals())

hubspot_pipeline()
