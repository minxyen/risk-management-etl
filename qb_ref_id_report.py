from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
import requests
import pandas as pd
import json
from log import config_logger

# logger = config_logger()

# TABLE_ID = 'bj7f569ni'
# REPORT_ID = '1000116'

def download_quickbase_report(QB_REALM_HOSTNAME, QB_USER_TOKEN, REPORT_ID, TABLE_ID, logger):
    headers = {
        'QB-Realm-Hostname': QB_REALM_HOSTNAME,
        'Authorization': f'QB-USER-TOKEN {QB_USER_TOKEN}'
        # 'Content-Type': 'application/json'
    }

    params = {
        'tableId': TABLE_ID
    }

    try:
        response = requests.post(
            f'https://api.quickbase.com/v1/reports/{REPORT_ID}/run',
            params=params,
            headers=headers
        )
        response.raise_for_status()  # Raise HTTPError if status code is not 2xx

        data = response.json()

        temp_list = []
        for i in data.get('data', []):
            row_values = [
                i.get('1021', {}).get('value', None),  # Disaster PW
                i.get('229', {}).get('value', None),   # Disaster
                i.get('242', {}).get('value', None),   # FEMA PW
                i.get('243', {}).get('value', None),   # ORM Ref
                i.get('3', {}).get('value', None),     # Record ID
                i.get('679', {}).get('value', None)    # FEMA Ref
            ]
            temp_list.append(row_values)

        record_id_report = pd.DataFrame(temp_list, columns=['Disaster PW', 'Disaster', 'FEMA PW', 'ORM Ref', 'Record ID#', 'FEMA Ref'])
        record_id_report.to_csv('record_id_report.csv', index=False)

        logger.info("[Ok] Downloaded Ref ID Report")
        return True

    except requests.exceptions.RequestException as req_ex:
        # Handle connection errors or timeout errors
        logger.error('Error occurred during the request:')
        logger.exception(req_ex)

    except json.JSONDecodeError as json_ex:
        # Handle JSON decoding errors
        logger.error('JSON Decoding Error:')
        logger.error(response.text)

    except Exception as ex:
        # Catch other unexpected exceptions
        logger.error('Unexpected Error:')
        logger.exception(ex)

    return False


# record_id_report = download_quickbase_report(QB_REALM_HOSTNAME, QB_USER_TOKEN, REPORT_ID, TABLE_ID, logger)

# '1021': Disaster PW
# '229': Disaster
# '242': FEMA PW
# '243': ORM Ref
# '3': Record ID#
# '679': FEMA Ref
