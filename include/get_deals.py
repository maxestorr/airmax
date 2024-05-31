# WIP testing hubspot deal search api requests
from pprint import pprint
from hubspot.crm import deals
from hubspot import hubspot
import json


from include.constants import HUBSPOT_ACCESS_TOKEN


api_client = hubspot.Client.create(access_token=HUBSPOT_ACCESS_TOKEN)

try:
    api_response = api_client.crm.deals.get_all()
    pprint(api_response[0])
    with open('data.json', 'w') as f:
        json.dump(api_response, f, default=str) # call __str__ on any non-serializable objects like datetime
except deals.ApiException as e:
    print("Exception when calling hubspot.crm.deals.get_all(): %s\n" % e)

