import pandas as pd
from log import config_logger

logger = config_logger()

target_file_name = 'Damages Export.csv'  # this will enventually be passed down from previous step.


# Read and select columns from the input CSV. # no Address, Project Title, Policy Issues.
damages = pd.read_csv(target_file_name)
damages = damages[['Damage #', 'Category', 'Name', 'Damage Description', 'Status',
                   'Cause of Damage', 'Latitude', 'Longitude', 'Event',
                   'Project #', 'County', 'Project Process Step',
                   'Site Inspectors', 'SI Status', 'Work Order #', 'Date Inspected',
                   'Date SI Report Approved', '% Work Complete', 'Imported DDD?',
                   'Has 406 Mitigation?', 'Insured?', 'Approx. Cost', 'CRC Gross Cost',
                   'Total 406 HMP Cost', 'Total Insurance Reductions', 'Federal Share',
                   'Non-Federal Share', 'Labor Type', 'Has EHP Concerns?',
                   '406 Mitigation Cost Type', '406 Mitigation Cost Effectiveness Type',
                   '406 Mitigation BCR', 'EHP Concerns Observed']]
# print(damages.columns)

damages['Disaster'] = damages['Event'].str[:4]
damages['Project #'] = damages['Project #'].fillna("").astype(str).str.replace('\.0$', '', regex=True)
# print(damages)


record_id_report = pd.read_csv('record_id_report.csv')
# print(record_id_report)

project_lookup = record_id_report[['FEMA Ref', 'Record ID#']]
project_lookup = project_lookup.rename(columns={'FEMA Ref':'Project #',
                                                'Record ID#': 'Related Project ID'})
project_lookup['Project #'] = project_lookup['Project #'].fillna("").astype(str).str.replace('\.0$', '', regex=True)
# project_lookup

merged_df = damages.merge(project_lookup, on='Project #', how='left')
merged_df['Related Project ID'] = merged_df['Related Project ID'].fillna("").astype(str).str.replace('\.0$', '', regex=True)
merged_df = merged_df.drop(columns=['Event'])
# merged_df.loc[merged_df['Project #'] == '', 'Related Project ID'] = ''
# print(merged_df)
merged_df.to_csv('merged_df.csv', index=False)

logger.info('[OK] Merged SharePoint Data and Ref ID Report')