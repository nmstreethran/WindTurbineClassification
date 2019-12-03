#%% [markdown]
# # Combining multiple csv files containing data into a single file

#%% [markdown]
# ## Downtime

#%%
import pandas as pd # import libraries

#%%
# import data as dataframes
df_lsm = pd.read_csv('data/Last_six_months_downtime.csv', skip_blank_lines=True)
df_pty = pd.read_csv('data/Prior_two_years_downtime.csv', skip_blank_lines=True)

#%%
# drop duplicate columns in data
df_pty = df_pty.drop('AvailabilityCategory_id.1',axis=1)
df_pty = df_pty.drop('EnvironmentalCategory_id.1', axis=1)
df_pty = df_pty.drop('GridCategory_id.1', axis=1)
df_pty = df_pty.drop('InfrastructureCategory_id.1', axis=1)
df_pty = df_pty.drop('TurbineCategory_id.1', axis=1)
df_pty = df_pty.drop('alarm_id.1', axis=1)
df_pty = df_pty.drop('comment.1', axis=1)
df_pty = df_pty.drop('id.1', axis=1)
df_pty = df_pty.drop('workorder_id.1', axis=1)
df_pty = df_pty.drop('turbine_id.1', axis=1)
df_pty = df_pty.drop('timestamp_end.1', axis=1)
df_pty = df_pty.drop('timestamp_start.1', axis=1)

#%%
# convert timestamps to datetime dtype
df_lsm['timestamp_start'] = pd.to_datetime(df_lsm['timestamp_start'])
df_lsm['timestamp_end'] = pd.to_datetime(df_lsm['timestamp_end'])
df_pty['timestamp_start'] = pd.to_datetime(df_pty['timestamp_start'])
df_pty['timestamp_end'] = pd.to_datetime(df_pty['timestamp_end'])

#%%
# concatenate both dataframes
df_dwntm = pd.concat([df_lsm, df_pty]) 
del df_lsm,df_pty

#%%
# sort by timestamp, then by turbine 
df_dwntm = df_dwntm.sort_values(['timestamp_start', 'timestamp_end', 'turbine_id'])

#%%
# reset index after sort
df_dwntm.reset_index(drop=True, inplace=True)

#%%
# save dataframe as new csv
df_dwntm.to_csv('data/downtime_merged.csv', index=False)
del df_dwntm