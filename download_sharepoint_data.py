from settings import ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER
from log import config_logger
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os
import fnmatch

# logger = config_logger()

def download_sharepoint_data(icf_username, icf_password, sp_site_url, sp_folder_url, wildcard_filename, logger):
    try:
        credentials = UserCredential(ICF_USERNAME, ICF_PASSWORD)
        ctx = ClientContext(SP_SITE_URL).with_credentials(credentials)

        # retrieve specific folder.
        list_source = ctx.web.get_folder_by_server_relative_url(SP_FOLDER_URL)
        logger.info(f'Complete SP Folder URL: {SP_SITE_URL}/{SP_FOLDER_URL}')
        files = list_source.files
        ctx.load(files)
        ctx.execute_query()

        file_names = [file.properties['Name'] for file in files]
        logger.info(f'All files in the folder: {file_names}')

        matching_files_names = fnmatch.filter(file_names, WILDCARD_FILENAME)
        downloaded_files = []

        for target_file_name in matching_files_names:
            target_file_url = SP_FOLDER_URL + "/" + target_file_name
            download_path = os.path.join(LOCAL_DATA_FOLDER, os.path.basename(target_file_url)).replace('\\', '/')

            with open(download_path, "wb") as local_file:
                file = ctx.web.get_file_by_server_relative_url(target_file_url).download(local_file).execute_query()

            logger.info(f"[OK] File has been downloaded into: {download_path}")
            downloaded_files.append(target_file_name)

        return downloaded_files

    except Exception as ex:
        logger.error('An error occurred during file download:')
        logger.exception(ex)
        return None

# output_files = download_sharepoint_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, logger)
#
# if output_files:
#     # Process the downloaded files as needed
#     for file_name in output_files:
#         # Your processing logic here...
#         logger.info(f'Processing downloaded file: {file_name}')
# else:
#     logger.error('No files were downloaded.')