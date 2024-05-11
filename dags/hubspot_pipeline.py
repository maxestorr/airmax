"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

import os
from airflow.decorators import dag, task
from pendulum import datetime
from hubspot import HubSpot
from dotenv import load_dotenv
import pandas as pd

from include.datasets import MY_FILE

load_dotenv()

HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

api_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)

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
        deals = api_client.crm.deals.get_all()
        deals = pd.DataFrame([deal.to_dict()['properties'] for deal in deals])
        deals.to_csv(MY_FILE)

    get_deals()

hubspot_pipeline()
