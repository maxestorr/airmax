# WIP testing hubspot deal search api requests
import hubspot

from dateutil import parser
from pprint import pprint
from hubspot.crm.contacts import PublicObjectSearchRequest, ApiException
from pendulum import datetime


from include.constants import HUBSPOT_ACCESS_TOKEN

api_client = hubspot.Client.create(access_token=HUBSPOT_ACCESS_TOKEN)

# timestamp in milliseconds
date = str(int(parser.isoparse("2024-05-24T00:00:00.000").timestamp() * 1000))
print(date)
pen_date = datetime(2024, 5, 24, 0, 0, 0, 0).int_timestamp * 1000
print(pen_date)

public_object_search_request = PublicObjectSearchRequest(
    filter_groups=[
        {
            "filters": [
                {
                    "value": date,
                    "propertyName": "lastmodifieddate",
                    "operator": "GTE"
                }
            ]
        }
    ], limit=10
)
try:
    api_response = api_client.crm.contacts.search_api.do_search(public_object_search_request=public_object_search_request)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling search_api->do_search: %s\n" % e)

