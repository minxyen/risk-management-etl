import os
from dotenv import load_dotenv
load_dotenv()

ICF_USERNAME = os.getenv('ICF_USERNAME')
ICF_PASSWORD = os.getenv('ICF_PASSWORD')


SP_SITE_URL = os.getenv('SP_SITE_URL')
SP_FOLDER_URL = os.getenv('SP_FOLDER_URL')

WILDCARD_FILENAME = os.getenv('WILDCARD_FILENAME')

LOCAL_DATA_FOLDER = os.getenv('LOCAL_DATA_FOLDER')

QB_REALM_HOSTNAME = os.getenv('QB_REALM_HOSTNAME')
QB_USER_TOKEN = os.getenv('QB_USER_TOKEN')

EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS')