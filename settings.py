import os
from dotenv import load_dotenv
load_dotenv()

ICF_USERNAME = os.getenv('ICF_USERNAME')
ICF_PASSWORD = os.getenv('ICF_PASSWORD')


SITE_URL = os.getenv('SITE_URL')
WILDCARD_FILENAME = os.getenv('WILDCARD_FILENAME')

LOCAL_DATA_FOLDER = os.getenv('LOCAL_DATA_FOLDER')