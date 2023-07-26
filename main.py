from settings import ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER
from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
from download_sharepoint_data import download_sharepoint_data
from qb_ref_id_report import download_quickbase_report
from merge_data import merge_data
from import_data import import_data
from archive_data import archive_data

from log import config_logger
logger = config_logger()

# Step 1:
output_files = download_sharepoint_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, logger)
if output_files:
    # Process the downloaded files as needed
    for file_name in output_files:
        # Your processing logic here...
        logger.info(f'Processing downloaded file: {file_name}')
else:
    logger.error('No files were downloaded.')


REPORT_ID = '1000116'
TABLE_ID = 'bj7f569ni'
record_id_report = download_quickbase_report(QB_REALM_HOSTNAME, QB_USER_TOKEN, REPORT_ID, TABLE_ID, logger)


merged_df = merge_data(logger)

file_name = 'merged_df.csv'
import_data(file_name, QB_REALM_HOSTNAME, QB_USER_TOKEN, logger)


archive_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, logger)