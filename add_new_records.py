from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
import requests
import pandas as pd

base_url = 'https://api.quickbase.com'

headers = {
    'QB-Realm-Hostname': QB_REALM_HOSTNAME,
    'Authorization': f'QB-USER-TOKEN {QB_USER_TOKEN}',
    'Content-Type': 'application/json'
}

url = f'{base_url}/v1/records'

df = pd.read_csv('merged_df.csv')
df = df.fillna("")

df['Approx. Cost'] = df['Approx. Cost'].apply(lambda x: x.replace("$","").replace(",",""))
df['CRC Gross Cost'] = df['CRC Gross Cost'].apply(lambda x: x.replace("$","").replace(",",""))
df['Federal Share'] = df['Federal Share'].apply(lambda x: x.replace("$","").replace(",","").replace("(","-").replace(")",""))
df['Non-Federal Share'] = df['Non-Federal Share'].apply(lambda x: x.replace("$","").replace(",","").replace("(","-").replace(")",""))

def percentage_to_decimal(percentage_str):
    if pd.isna(percentage_str) or percentage_str == '':
        return ''
    return str(float(percentage_str.strip('%')) / 100)
df['% Work Complete'] = df['% Work Complete'].apply(percentage_to_decimal)

# Dictionary to map values to their corresponding boolean values
mapping = {'Yes': True, 'No': False}
df['Imported DDD?'] = [mapping.get(value, None) for value in df['Imported DDD?']]


df['Date Inspected'] = pd.to_datetime(df['Date Inspected'], format='%m/%d/%Y %I:%M %p', errors='coerce')
df['Date Inspected'] = df['Date Inspected'].dt.strftime('%Y-%m-%d').fillna('')

df['Date SI Report Approved'] = pd.to_datetime(df['Date SI Report Approved'], format='%m/%d/%Y %I:%M %p', errors='coerce')
df['Date SI Report Approved'] = df['Date SI Report Approved'].dt.strftime('%Y-%m-%d').fillna('')

df = df[df['Federal Share'].str.contains('-')]


for index, row in df.iterrows():
    # print(row)
    damage_no = row['Damage #']
    category = row['Category']
    name = row['Name']
    damage_description = row['Damage Description']
    status = row['Status']
    cause_of_damage = row['Cause of Damage']
    latitude = row['Latitude']
    longitude = row['Longitude']
    project_no = row['Project #']
    county = row['County']
    project_process_step = row['Project Process Step']
    site_inspectors = row['Site Inspectors']
    si_status = row['SI Status']
    work_order_no = row['Work Order #']
    date_inspected = row['Date Inspected']
    date_si_report_approved = row['Date SI Report Approved']
    perc_work_complete = row['% Work Complete']     # need to think about when there is null values.
    imported_ddd = row['Imported DDD?']
    has_406_mitigation = row['Has 406 Mitigation?']
    insured = row['Insured?']
    approx_cost = row['Approx. Cost']
    crc_gross_cost = row['CRC Gross Cost']
    total_406_hmp_cost = row['Total 406 HMP Cost']
    total_insurance_reductions = row['Total Insurance Reductions']
    federal_share = row['Federal Share']
    non_federal_share = row['Non-Federal Share']
    labor_type = row['Labor Type']                      # need to deal with field type - text multiple choice restriction.
    has_emp_concerns = row['Has EHP Concerns?']
    mitigation_406_cost_type = row['406 Mitigation Cost Type']
    mitigation_406_cost_effectiveness_type = row['406 Mitigation Cost Effectiveness Type']
    mitigation_406_bcr = row['406 Mitigation BCR']
    ehp_concerns_observed = row['EHP Concerns Observed']
    disaster = row['Disaster']
    related_project_id = row['Related Project ID']


    payload = {
        "to": "btfz6vxv2",
        "data": [
            {
            "26": {"value": damage_no},
            "31": {"value": category},
            "9": {"value": name},
            "19": {"value": damage_description},
            "92": {"value": status},
            "34": {"value": cause_of_damage},
            "17": {"value": latitude},
            "18": {"value": longitude},
            "33": {"value": project_no},
            "107": {"value": county},
            "113": {"value": project_process_step},
            "114": {"value": site_inspectors},
            "115": {"value": si_status},
            "116": {"value": work_order_no},
            "117": {"value": date_inspected},    # correct format and are valid choices ???
            "118": {"value": date_si_report_approved},
            "22": {"value": perc_work_complete},  # %
            "119": {"value": imported_ddd},
            "80": {"value": has_406_mitigation},
            "37": {"value": insured},
            "21": {"value": approx_cost},    # currency
            "81": {"value": crc_gross_cost},  # currency
            "82": {"value": total_406_hmp_cost},
            "83": {"value": total_insurance_reductions},
            "85": {"value": federal_share},  # currency
            "108": {"value": non_federal_share},  # currency
            "23": {"value": labor_type},
            "86": {"value": has_emp_concerns},
            "87": {"value": mitigation_406_cost_type},
            "88": {"value": mitigation_406_cost_effectiveness_type},
            "120": {"value": mitigation_406_bcr},
            "90": {"value": ehp_concerns_observed},
            "28": {"value": disaster},
            "139": {"value": related_project_id}
            }
        ]
    }
    print(payload)

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
        print('---------')
        # Process the returned data as needed
    else:
        print('Error:', response)
        print('Error:', response.status_code)
        print('Error:', response.reason)
        print('Error:', response.text)
        print('---------------------')
        # print(payload)
        print('=====================')


    # break


    ## Damage No.                     26. Text. Key.
    ## Category                       31. Text - Multiple Choice. (A, B, C, D, E, F, G, Z, N/A, '')  -user can not add  -- df[df['Category']=='MCGUIRE, GEORGE P.']
    ## Name                           9. Text - Multi-line
    ## Damage Description             19. Text - Multi-line
    ## Status                         92. Text - Multi-line
    ## Cause of Damage                34. Text - Multiple Choice (Hurricane, Winter Storm, Tropical Storm, Flood, Tornado, Severe Storm, Wind, '') - user can add   --df[df['Cause of Damage']=='8/24/2021 09:52 PM']
    ## Latitude                       17. Text
    ## Longitude                      18. Text
    ## Project #                      33. Numeric
    ## County                         107. Text - Multiple Choice (East Baton Rouge Parish, Jefferson, '') - user can add  -- df[df['County']=='Unanswered']
    ## Project Process Step           113. Text - Multiple Choice (Obligated, Process Discontinued, Pending Applicant DDD Approval, Pending CRC Project Development, Pending PDMG Project Review, Pending Initial Project Development, Pending DDD Completion, Pending PDMG Scope & Cost Routing, Pending Applicant Project Review, Pending Peer Review, Pending Large Project Review, Pending Formulation Completion, Applicant Signed Project, Pending EHP Review, Pending Insurance Completion, Pending QA Review, Pending Final FEMA Review, Pending FEMA 406 HMP Completion, Pending Applicant 406 HMP Completion, Pending EMMIE Submission, '') - user can add   --df[df['Project Process Step']=='$2,329.19']
    ## Site Inspectors                114. Text
    ## SI Status                      115. Text
    ## Work Order #                   116. Numeric.
    ## Date Inspected                 117. Date.
    ## Date SI Report Approved        118. Date.
    ## % Work Complete                22. Percent.
    ## Imported DDD?                  119. Checkbox.
    ## Has 406 Mitigation?            80. Text - Multiple Choice (No, Yes, '') - user can add   --all good here
    ## Insured?                       37. Text.
    ## Approx. Cost                   21. Currency.
    ## CRC Gross Cost                 81. Currency.
    ## Total 406 HMP Cost             82. Currency.
    ## Total Insurance Reductions     83. Currency.
    ## Federal Share                  85. Currency.
    ## Non-Federal Share              108. Currency.
    ## Labor Type                     23. Text - Multiple Choice (MAA, MA, MOU, FA, C, FA/C, DR, '')  - user can not add  --all wrong.
    ## Has EHP Concerns?              86. Text - Multiple Choice (Yes, N/A, No, Unknown, '') - user can add  --all good
    ## 406 Mitigation Cost Type       87. Text - Multiple Choice (Supplement Repair Cost, '')  - user can add  --all good
    ## 406 Mitigation Cost Effectiveness Type    88. Text - Multiple Choice (100% Rule, 15% Rule, '') - user can add  --all good
    ## 406 Mitigation BCR             120. Text.
    ## EHP Concerns Observed          90. Text.
    ## Disaster                       28. Text - Multiple Choice (4570, 1607, 4577, 4590, 4559, 4606, 4611, 4345, 4439, 4458, '') user can not add  --all good
    ## Related Project ID             Related Project (Record ID#). 6. Numeric.   (139 for test)
