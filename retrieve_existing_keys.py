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

TABLE_ID = 'brbauvppt'
TABLE_KEY = [26]


body = {"from":TABLE_ID,"select": TABLE_KEY}

response = requests.post(
	'https://api.quickbase.com/v1/records/query',
	headers = headers,
	json = body
)

# print(json.dumps(r.json(),indent=4))

data = response.json()
# print(data)

existing_key_list = []
for i in data['data']:
	damage_no = i.get('26', {}).get('value', None) # Damage No.
	existing_key_list.append(damage_no)

# may need to check if there are any duplicates (protection)
# print(existing_key_list)

df = pd.DataFrame(existing_key_list, columns=['Damage No.'])
print(df)
df.to_csv('existing_key_list.csv', index=False)

logger.info("[OK] Downloaded Existing Key List")