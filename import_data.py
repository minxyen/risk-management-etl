from settings import QB_REALM_HOSTNAME, QB_USER_TOKEN
from send_outlook_email import send_outlook_email

import requests
import pandas as pd
import json

# from log import config_logger
# logger = config_logger()

def import_data(file_name, QB_REALM_HOSTNAME, QB_USER_TOKEN, EMAIL_RECIPIENTS, logger):
    headers = {
        'QB-Realm-Hostname': QB_REALM_HOSTNAME,
        'Authorization': f'QB-USER-TOKEN {QB_USER_TOKEN}',
        'Content-Type': 'application/json'
    }

    url = 'https://api.quickbase.com/v1/records'

    df = pd.read_csv(file_name)
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

    mapping = {'Contract': 'C',
               'Force Account and Contract': 'FA/C',
               'Force Account': 'FA',
               'Donated Resources': 'DR',
               'Mutual Aid': 'MAA',
               'Mission Assigned': 'MA',
               'Memorandum of Understanding': 'MOU'}

    df['Labor Type'] = [mapping.get(value, None) for value in df['Labor Type']]


    df['Date Inspected'] = pd.to_datetime(df['Date Inspected'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    df['Date Inspected'] = df['Date Inspected'].dt.strftime('%Y-%m-%d').fillna('')

    df['Date SI Report Approved'] = pd.to_datetime(df['Date SI Report Approved'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    df['Date SI Report Approved'] = df['Date SI Report Approved'].dt.strftime('%Y-%m-%d').fillna('')


    data_list = []
    for index, row in df.iterrows():
        # print(row)
        data_dict = {
            "26": {"value": row['Damage #']},
            "31": {"value": row['Category']},
            "9": {"value": row['Name']},
            "19": {"value": row['Damage Description']},
            "92": {"value": row['Status']},
            "34": {"value": row['Cause of Damage']},
            "17": {"value": row['Latitude']},
            "18": {"value": row['Longitude']},
            "33": {"value": row['Project #']},
            "107": {"value": row['County']},
            "113": {"value": row['Project Process Step']},
            "114": {"value": row['Site Inspectors']},
            "115": {"value": row['SI Status']},
            "116": {"value": row['Work Order #']},
            "117": {"value": row['Date Inspected']},  # Format and validation should be done before this step
            "118": {"value": row['Date SI Report Approved']},  # Format and validation should be done before this step
            "22": {"value": row['% Work Complete']},  # Format and validation should be done before this step
            "119": {"value": row['Imported DDD?']},
            "80": {"value": row['Has 406 Mitigation?']},
            "37": {"value": row['Insured?']},
            "21": {"value": row['Approx. Cost']},  # Format and validation should be done before this step
            "81": {"value": row['CRC Gross Cost']},  # Format and validation should be done before this step
            "82": {"value": row['Total 406 HMP Cost']},
            "83": {"value": row['Total Insurance Reductions']},
            "85": {"value": row['Federal Share']},  # Format and validation should be done before this step
            "108": {"value": row['Non-Federal Share']},  # Format and validation should be done before this step
            "23": {"value": row['Labor Type']},
            "86": {"value": row['Has EHP Concerns?']},
            "87": {"value": row['406 Mitigation Cost Type']},
            "88": {"value": row['406 Mitigation Cost Effectiveness Type']},
            "120": {"value": row['406 Mitigation BCR']},
            "90": {"value": row['EHP Concerns Observed']},
            "28": {"value": row['Disaster']},
            "139": {"value": row['Related Project ID']}
        }
        # Append the data_dict to the data_list
        data_list.append(data_dict)

    payload = {
        "to": "btfz6vxv2",   #    brbauvppt
        "data": data_list
    }
    # print(payload)

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError if status code is not 2xx

        data = response.json()
        logger.info(data)
        # Process the returned data as needed
        logger.info('[OK] Data Import Finished!!')
        send_outlook_email(EMAIL_RECIPIENTS, 'Damages Data Import Success',
                           'The damages data import process has been completed successfully.', logger)

    except requests.exceptions.RequestException as req_ex:  # These errors can occur due to network issues or server unavailability
        # Handle connection errors or timeout errors
        logger.error('Error occurred during the request:')
        logger.exception(req_ex)
        send_outlook_email(EMAIL_RECIPIENTS, 'Damages Data Import Failure',
                           'The damages data import process encountered an error. Please check the logs for details.', logger)


    except json.JSONDecodeError as json_ex:   # this might raise a JSONDecodeError if the response is not a valid JSON.
        # Handle JSON decoding errors
        logger.error('JSON Decoding Error:')
        logger.error(response.text)
        send_outlook_email(EMAIL_RECIPIENTS, 'Damages Data Import Failure',
                           'The damages data import process encountered an error. Please check the logs for details.', logger)

    except Exception as ex:
        # Catch other unexpected exceptions
        logger.error('Unexpected Error:')
        logger.exception(ex)    # log the full traceback, which provides more detailed information about the error.
        # logger.error(f'Payload: {payload}')
        send_outlook_email(EMAIL_RECIPIENTS, 'Damages Data Import Failure',
                           'The damages data import process encountered an error. Please check the logs for details.', logger)


    ## Damage No.                     26. Text. Key.
    ## Category                       31. Text - Multiple Choice. (A, B, C, D, E, F, G, Z, N/A, '')  -user can not add
    ## Name                           9. Text - Multi-line
    ## Damage Description             19. Text - Multi-line
    ## Status                         92. Text - Multi-line
    ## Cause of Damage                34. Text - Multiple Choice (Hurricane, Winter Storm, Tropical Storm, Flood, Tornado, Severe Storm, Wind, '') - user can add
    ## Latitude                       17. Text
    ## Longitude                      18. Text
    ## Project #                      33. Numeric
    ## County                         107. Text - Multiple Choice (East Baton Rouge Parish, Jefferson, '') - user can add
    ## Project Process Step           113. Text - Multiple Choice (Obligated, Process Discontinued, Pending Applicant DDD Approval, Pending CRC Project Development, Pending PDMG Project Review, Pending Initial Project Development, Pending DDD Completion, Pending PDMG Scope & Cost Routing, Pending Applicant Project Review, Pending Peer Review, Pending Large Project Review, Pending Formulation Completion, Applicant Signed Project, Pending EHP Review, Pending Insurance Completion, Pending QA Review, Pending Final FEMA Review, Pending FEMA 406 HMP Completion, Pending Applicant 406 HMP Completion, Pending EMMIE Submission, '') - user can add
    ## Site Inspectors                114. Text
    ## SI Status                      115. Text
    ## Work Order #                   116. Numeric.
    ## Date Inspected                 117. Date.
    ## Date SI Report Approved        118. Date.
    ## % Work Complete                22. Percent.
    ## Imported DDD?                  119. Checkbox.
    ## Has 406 Mitigation?            80. Text - Multiple Choice (No, Yes, '') - user can add
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
