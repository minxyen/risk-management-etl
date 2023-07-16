from settings import ICF_USERNAME, ICF_PASSWORD

from office365.runtime.auth.user_credential import UserCredential
# The ClientContext class is used to interact with SharePoint data and services.
from office365.sharepoint.client_context import ClientContext


site_url = 'https://icfonline.sharepoint.com/sites/DMTechnologyStandards'
credentials = UserCredential(ICF_USERNAME, ICF_PASSWORD)
ctx = ClientContext(site_url).with_credentials(credentials)

# retrieve specific folder.
list_source = ctx.web.get_folder_by_server_relative_url(
    'Shared Documents/1. Program & Project Support/B. Client Specific/LA ORM/Data/Damages')
files = list_source.files
ctx.load(files)

# This line sends the request to SharePoint to execute the operations accumulated in the context (ctx) so far.
# This is known as "batching" and is commonly used to improve performance when working with SharePoint.
ctx.execute_query()

for file in files:
    print(file.properties['Name'])
