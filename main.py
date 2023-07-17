from settings import ICF_USERNAME, ICF_PASSWORD, SITE_URL, WILDCARD_FILENAME, LOCAL_DATA_FOLDER

from office365.runtime.auth.user_credential import UserCredential
# The ClientContext class is used to interact with SharePoint data and services.
from office365.sharepoint.client_context import ClientContext
from pathlib import Path

import os
import fnmatch

# site_url = 'https://icfonline.sharepoint.com/sites/DMTechnologyStandards'
credentials = UserCredential(ICF_USERNAME, ICF_PASSWORD)
ctx = ClientContext(SITE_URL).with_credentials(credentials)

folder_url = 'Shared Documents/1. Program & Project Support/B. Client Specific/LA ORM/Data/Damages'
print('folder_url:', folder_url)

# retrieve specific folder.
list_source = ctx.web.get_folder_by_server_relative_url(folder_url)
files = list_source.files
ctx.load(files)
#
# # This line sends the request to SharePoint to execute the operations accumulated in the context (ctx) so far.
# # This is known as "batching" and is commonly used to improve performance when working with SharePoint.
ctx.execute_query()
file_names = [file.properties['Name'] for file in files]
print('file_names:', file_names)

# wildcard_filename = "*damage*"
matching_files_names = fnmatch.filter(file_names, WILDCARD_FILENAME)
target_file_name = matching_files_names[-1]
print('target_file_name:', target_file_name)


target_file_url = folder_url + "/" + target_file_name
print('target_file_url:', target_file_url)

# print(Path.home())
# local_data_folder = os.path.join(Path.home(), r'Documents\ICF\Automation\Damages')
print('local_data_folder:', LOCAL_DATA_FOLDER)

download_path = os.path.join(LOCAL_DATA_FOLDER, os.path.basename(target_file_url)).replace('\\', '/')
print('download_path:', download_path)
# C:/Users/60788/Documents/ICF/Automation/Damages/Damages Export.csv

# This line opens a file on the local file system for writing in binary mode.
with open(download_path, "wb") as local_file:
    file = ctx.web.get_file_by_server_relative_url(target_file_url).download(local_file).execute_query()

print("[Ok] file has been downloaded into: {0}".format(download_path))
