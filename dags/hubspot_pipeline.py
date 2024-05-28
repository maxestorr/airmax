"""
## hubspot_pipeline.py

Take daily snapshots of hubspot tables.
"""

# TODO: remove top level code including expensive imports

import json
from airflow.decorators import dag, task
from pendulum import datetime
from hubspot import HubSpot
from hubspot.crm import deals
from hubspot.crm import deals
# import pandas as pd
from dateutil import parser

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
        # TODO:
        #  Handle potential errors
        #  use logs instead of print
        hubspot_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)

        # timestamp in milliseconds
        first_date = str(int(parser.isoparse("2024-05-20T00:00:00.000").timestamp() * 1000))
        last_date = str(int(parser.isoparse("2024-05-27T00:00:00.000").timestamp() * 1000))
        public_object_search_request = deals.PublicObjectSearchRequest(
            filter_groups=[
                {
                    "filters": [
                        {
                            "propertyName": "lastmodifieddate",
                            "operator": "GTE",
                            "value": first_date,
                        },
                        {
                            "propertyName": "lastmodifieddate",
                            "operator": "LT",
                            "value": last_date,
                        },
                    ]
                }
            ], limit=10 # TODO: remove limit before deployment
        )

        try:
            api_response = hubspot_client.crm.deals.search_api.do_search(public_object_search_request=public_object_search_request)
            # pprint(api_response)
            with open(MY_FILE, "w+") as f:
                json.dump(api_response, f)

        except deals.ApiException as e:
            print(f"Exception when calling deals.search_api->do_search: {e}\n")

        print(f"Saved snapshot [TIMESTAMP] to location {MY_FILE}\n")

    get_deals()

hubspot_pipeline()

# WIP testing hubspot deal search api requests


