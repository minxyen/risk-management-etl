import pandas as pd

target_file_name = 'Damages Export.csv'

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
print(damages)

# no Address, Project Title, Policy Issues