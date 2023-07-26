from settings import ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER
from log import config_logger

from office365.runtime.auth.user_credential import UserCredential
# The ClientContext class is used to interact with SharePoint data and services.
from office365.sharepoint.client_context import ClientContext
from datetime import datetime

# logger = config_logger()


def archive_data(icf_username, icf_password, sp_site_url, sp_folder_url, logger):
    credentials = UserCredential(icf_username, icf_password)
    ctx = ClientContext(sp_site_url).with_credentials(credentials)

    # get a source file located in library 'Shared Documents'
    source_file = ctx.web.get_file_by_server_relative_url(f"{sp_folder_url}/Damages Export.csv")

    # move the file into the archive folder. with datetime in the end of folder name.
    now = datetime.now()
    formatted_datetime = now.strftime("%Y%m%d")
    source_file.moveto(f"{sp_folder_url}/Archive/{formatted_datetime}", 1)  # 1 means "overwrite" a file with the same name if it exists
    # execute a query
    ctx.execute_query()

    logger.info("[OK] File has been archived.")
