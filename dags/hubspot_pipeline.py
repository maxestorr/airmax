"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

from airflow.decorators import dag, task
from pendulum import datetime

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
        pass

    get_deals()

hubspot_pipeline()
