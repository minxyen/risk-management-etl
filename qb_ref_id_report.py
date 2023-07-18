from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
import requests
import pandas as pd
import json
from pprint import pprint

base_url = 'https://api.quickbase.com'

headers = {
    'QB-Realm-Hostname': QB_REALM_HOSTNAME,
    'Authorization': f'QB-USER-TOKEN {QB_USER_TOKEN}'
    # 'Content-Type': 'application/json'
}

print(headers)

TABLE_ID = 'bj7f569ni'
REPORT_ID = '1000116'
url = f'{base_url}/records/query'

params = {
  	'tableId': TABLE_ID
}

response = requests.post(
        f'{base_url}/v1/reports/{REPORT_ID}/run',
        params = params,
        headers = headers
    )

print(response)
data = response.json()

for i in data['data']:
    print(i)


# '1021': Disaster PW
# '229': Disaster
# '242': FEMA PW
# '243': ORM Ref
# '3': Record ID#
# '679': FEMA Ref
