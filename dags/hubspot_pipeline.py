"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

import json

from airflow.decorators import dag, task
from pendulum import datetime
import hubspot
from hubspot.crm import deals

from include.constants import (
    HUBSPOT_ACCESS_TOKEN,
    MY_FILE
)


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
    def get_deals() -> None:
        hubspot_client = hubspot.Client.create(access_token=HUBSPOT_ACCESS_TOKEN)

        try:
            api_response = hubspot_client.crm.deals.get_all()
            with open(MY_FILE, "w") as f:
                json.dump(api_response, f, default=str)

        except deals.ApiException as e:
            print(f"Exception when calling hubspot.crm.deals.get_all(): {e}\n")

        print(f"Saved snapshot [TIMESTAMP] to location {MY_FILE}\n")

    get_deals()

hubspot_pipeline()

# WIP testing hubspot deal search api requests


