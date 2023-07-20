import pandas as pd

merged_df = pd.read_csv('merged_df.csv')
existing_key_list = pd.read_csv('existing_key_list.csv')


existing_key_list = existing_key_list['Damage No.'].to_list()

merged_df['Existing'] = merged_df['Damage #'].isin(existing_key_list).astype(int)
# print(merged_df)
existing_data = merged_df[merged_df['Existing']==1]
# existing_data.to_csv('existing_data.csv', index=False)

new_data = merged_df[merged_df['Existing']==0]
# new_data.to_csv('new_data.csv', index=False)

for index, row in merged_df.iterrows():
    print(row)





## Damage No.                     26. Text. Key.
## Category                       31. Text - Multiple Choice. (A, B, E, G, F, D, C, Z, N/A)
## Name                           8. Text - Multi-line
## Damage Description             19. Text - Multi-line
## Status                         92. Text - Multi-line
## Cause of Damage                34. Text - Multiple Choice (Hurricane, Winter Storm, Tropical Storm, Flood, Tornado, Severe Storm, Wind) - user can add
## Latitude                       17. Text
## Longitude                      18. Text
## Project #                      33. Numeric
## County                         107. Text - Multiple Choice (East Baton Rouge Parish, Jefferson) - user can add
## Project Process Step           113. Text - Multiple Choice (Obligated, Process Discontinued, Pending Applicant DDD Approval, Pending CRC Project Development, Pending PDMG Project Review, Pending Initial Project Development, Pending DDD Completion, Pending PDMG Scope & Cost Routing, Pending Applicant Project Review, Pending Peer Review, Pending Large Project Review, Pending Formulation Completion, Applicant Signed Project, Pending EHP Review, Pending Insurance Completion, Pending QA Review, Pending Final FEMA Review, Pending FEMA 406 HMP Completion, Pending Applicant 406 HMP Completion, Pending EMMIE Submission) - user can add
## Site Inspectors                114. Text
## SI Status                      115. Text
## Work Order #                   116. Numeric.
## Date Inspected                 117. Date.
## Date SI Report Approved        118. Date.
## % Work Complete                22. Percent.
## Imported DDD?                  119. Checkbox.
## Has 406 Mitigation?            80. Text - Multiple Choice (No, Yes) - user can add
## Insured?                       37. Text.
## Approx. Cost                   21. Currency.
## CRC Gross Cost                 81. Currency.
## Total 406 HMP Cost             82. Currency.
## Total Insurance Reductions     83. Currency.
## Federal Share                  85. Currency.
## Non-Federal Share              108. Currency.
## Labor Type                     23. Text - Multiple Choice (MAA, MA, MOU, FA, C, FA/C, DR)  - user can not add
## Has EHP Concerns?              86. Text - Multiple Choice (Yes, N/A, No, Unknown) - user can add
## 406 Mitigation Cost Type       87. Text - Multiple Choice (Supplement Repair Cost)
## 406 Mitigation Cost Effectiveness Type    88. Text - Multiple Choice (100% Rule, 15% Rule) - user can add
## 406 Mitigation BCR             120. Text.
## EHP Concerns Observed          90. Text.
## Disaster                       28. Text - Multiple Choice (4570, 1607, 4577, 4590, 4559, 4606, 4611, 4345, 4439, 4458) user can not add
## Related Project ID             Related Project (Record ID#). 6. Numeric.   (139 for test)




