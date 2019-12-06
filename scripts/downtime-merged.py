#%% [markdown]
# # Combining multiple csv files containing data into a single file

#%% [markdown]
# ## Downtime

#%%
# import libraries
import pandas as pd

#%%
# import data as dataframes
dt_l6m = pd.read_csv(
    'data/Last_six_months_downtime.csv', skip_blank_lines=True)
dt_p2y = pd.read_csv(
    'data/Prior_two_years_downtime.csv', skip_blank_lines=True)

#%%
# drop duplicate columns in data
dt_p2y = dt_p2y[dt_p2y.columns.drop(list(dt_p2y.filter(regex='.1')))]

#%%
# convert timestamps to datetime dtype
dt_l6m['timestamp_start'] = pd.to_datetime(dt_l6m['timestamp_start'])
dt_l6m['timestamp_end'] = pd.to_datetime(dt_l6m['timestamp_end'])
dt_p2y['timestamp_start'] = pd.to_datetime(dt_p2y['timestamp_start'])
dt_p2y['timestamp_end'] = pd.to_datetime(dt_p2y['timestamp_end'])

#%%
# concatenate both dataframes
dwntm = pd.concat([dt_l6m, dt_p2y]) 
del dt_l6m,dt_p2y

#%%
# sort by timestamp, then by turbine 
dwntm = dwntm.sort_values(
    ['timestamp_start', 'timestamp_end', 'turbine_id'])

#%%
# reset index after sort
dwntm.reset_index(drop=True, inplace=True)

#%%
# save dataframe as new csv
dwntm.to_csv('data/downtime_merged.csv', index=False)
del dwntm
