from settings import ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER
from log import config_logger

from office365.runtime.auth.user_credential import UserCredential
# The ClientContext class is used to interact with SharePoint data and services.
from office365.sharepoint.client_context import ClientContext
from pathlib import Path

import os
import fnmatch

logger = config_logger()
def download_sharepoint_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, logger):
    credentials = UserCredential(ICF_USERNAME, ICF_PASSWORD)
    ctx = ClientContext(SP_SITE_URL).with_credentials(credentials)

    # retrieve specific folder.
    list_source = ctx.web.get_folder_by_server_relative_url(SP_FOLDER_URL)
    # print('Complete SP Folder URL:', SP_SITE_URL + '/' + SP_FOLDER_URL)
    logger.info(f'Complete SP Folder URL: {SP_SITE_URL}/{SP_FOLDER_URL}')
    files = list_source.files
    ctx.load(files)
    #
    # # This line sends the request to SharePoint to execute the operations accumulated in the context (ctx) so far.
    # # This is known as "batching" and is commonly used to improve performance when working with SharePoint.
    ctx.execute_query()
    file_names = [file.properties['Name'] for file in files]
    logger.info(f'All files in the folder: {file_names}')

    # wildcard_filename = "*damage*"
    matching_files_names = fnmatch.filter(file_names, WILDCARD_FILENAME)
    target_file_name = matching_files_names[-1]
    logger.info(f'Target file names based on wildcard search: {target_file_name}')

    target_file_url = SP_FOLDER_URL + "/" + target_file_name

    # print(Path.home())
    # local_data_folder = os.path.join(Path.home(), r'Documents\ICF\Automation\Damages')
    # print('local_data_folder:', LOCAL_DATA_FOLDER)

    download_path = os.path.join(LOCAL_DATA_FOLDER, os.path.basename(target_file_url)).replace('\\', '/')
    logger.info(f'Download data to local: {download_path}')
    # C:/Users/60788/Documents/ICF/Automation/Damages/Damages Export.csv

    # This line opens a file on the local file system for writing in binary mode.
    with open(download_path, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_url(target_file_url).download(local_file).execute_query()

    logger.info("[Ok] file has been downloaded into: {0}".format(download_path))
    return target_file_name


output_file_name = download_sharepoint_data(ICF_USERNAME, ICF_PASSWORD, SP_SITE_URL, SP_FOLDER_URL, WILDCARD_FILENAME, logger)


# the output should return the target_file_name and pass it to the next step.
# Need to think about how to read in multiple files -> most likely using a loop and return all the files names in a list.
