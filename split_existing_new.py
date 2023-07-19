import pandas as pd

merged_df = pd.read_csv('merged_df.csv')
existing_key_list = pd.read_csv('existing_key_list.csv')


existing_key_list = existing_key_list['Damage No.'].to_list()

merged_df['Existing'] = merged_df['Damage #'].isin(existing_key_list).astype(int)
# print(merged_df)
existing_data = merged_df[merged_df['Existing']==1]
existing_data.to_csv('existing_data.csv', index=False)

new_data = merged_df[merged_df['Existing']==0]
new_data.to_csv('new_data.csv', index=False)



