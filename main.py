from settings import ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER
from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
from settings import EMAIL_RECIPIENTS
from download_sharepoint_data import download_sharepoint_data
from qb_ref_id_report import download_quickbase_report
from merge_data import merge_data
from import_data import import_data
from archive_data import archive_data
from send_outlook_email import send_outlook_email

from log import config_logger
logger = config_logger()

def main():

    try:
        # Step 1:
        download_sharepoint_success = download_sharepoint_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, logger)
        if download_sharepoint_success:
            # Step 2
            REPORT_ID = '1000116'
            TABLE_ID = 'bj7f569ni'
            download_quickbase_report_success = download_quickbase_report(QB_REALM_HOSTNAME, QB_USER_TOKEN, REPORT_ID, TABLE_ID, logger)
        else:
            download_quickbase_report_success = False

        if download_quickbase_report_success:
            # Step 3
            merge_success = merge_data(logger)
        else:
            merge_success = False

        if merge_success:
            # Step 4
            file_name = 'merged_df.csv'
            import_success = import_data(file_name, QB_REALM_HOSTNAME, QB_USER_TOKEN, EMAIL_RECIPIENTS, logger)
        else:
            import_success = False

        # Step 5
        if import_success:
            archive_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, logger)

        # # Step 6
        # recipients = ['minyen.hsieh@icf.com']
        # send_outlook_email(recipients, 'test', 'test', logger)

    except Exception as ex:
        # Catch other unexpected exceptions
        logger.error('Unexpected Error:')
        logger.exception(ex)
        send_outlook_email(EMAIL_RECIPIENTS, 'Damages Data Import Failure',
                           'The damages data import process encountered an error. Please check the logs for details.',
                           logger)

if __name__ == "__main__":
    main()