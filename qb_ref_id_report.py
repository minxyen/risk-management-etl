from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
import requests
import pandas as pd

from log import config_logger
logger = config_logger()

headers = {
    'QB-Realm-Hostname': QB_REALM_HOSTNAME,
    'Authorization': f'QB-USER-TOKEN {QB_USER_TOKEN}'
    # 'Content-Type': 'application/json'
}

# print(headers)

TABLE_ID = 'bj7f569ni'
params = {
  	'tableId': TABLE_ID
}

REPORT_ID = '1000116'
response = requests.post(
        f'https://api.quickbase.com/v1/reports/{REPORT_ID}/run',
        params = params,
        headers = headers
    )
# print(response)
data = response.json()

temp_list = []
for i in data['data']:
    row_values = [
        i.get('1021', {}).get('value', None),  # Disaster PW
        i.get('229', {}).get('value', None),   # Disaster
        i.get('242', {}).get('value', None),   # FEMA PW
        i.get('243', {}).get('value', None),   # ORM Ref
        i.get('3', {}).get('value', None),     # Record ID
        i.get('679', {}).get('value', None)    # FEMA Ref
    ]
    # Uncomment the following lines if you want to check for missing values
    # if None in row_values:
    #     print("Missing value warning!")
    temp_list.append(row_values)

df = pd.DataFrame(temp_list, columns=['Disaster PW', 'Disaster', 'FEMA PW', 'ORM Ref', 'Record ID#', 'FEMA Ref'])
df.to_csv('record_id_report.csv', index=False)
# print(df)
logger.info("[Ok] Downloaded Ref ID Report")

# '1021': Disaster PW
# '229': Disaster
# '242': FEMA PW
# '243': ORM Ref
# '3': Record ID#
# '679': FEMA Ref
