#%% [markdown]
# # Combining multiple csv files containing data into a single file

#%% [markdown]
# ## SCADA

#%%
import pandas as pd # import libraries
import numpy as np
import itertools

#%%
# import data - versions 1 (old) and 2 (new)
df_v11 = pd.read_csv('data/Last_six_months_SCADA.csv', skip_blank_lines=True)
df_v12 = pd.read_csv('data/Prior_two_years_SCADA.csv', skip_blank_lines=True)
df_v21 = pd.read_csv('data/NS_SCADA_v2.csv', skip_blank_lines=True)
df_v22 = pd.read_csv('data/NS_SCADA_2017_v2.csv', skip_blank_lines=True)

#%%
# return columns and their dtypes for each dataframe
df_v11.dtypes, df_v12.dtypes, df_v21.dtypes, df_v22.dtypes

#%%
# return shapes of each dataframe
df_v11.shape, df_v12.shape, df_v21.shape, df_v22.shape

#%%
# rename ap_min in df_v12 to ap_max
df_v12.rename(columns={'ap_min': 'ap_max'}, inplace=True)

#%%
# fixing rotor speed readings due to errors in data
def f_m1(c): # define function to merge some old rotor speed readings with new data
    if c['turbine'] <= 20:
        return c['rs_av']
df_v11['rs_av_old'] = df_v11.apply(f_m1, axis=1)
df_v12['rs_av_old'] = df_v12.apply(f_m1, axis=1)

#%%
df_v11 = df_v11.drop('rs_av', axis=1) # delete original columns
df_v12 = df_v12.drop('rs_av', axis=1)

#%%
# concatenate two df_v1 to one
df_v1 = pd.concat([df_v11, df_v12]) # old SCADA
df_v2 = pd.concat([df_v21, df_v22]) # new SCADA
del df_v11, df_v12, df_v21, df_v22 # delete concatenated dataframes from memory

#%%
df_v2['timestamp'] = pd.to_datetime(df_v2['timestamp']) # convert timestamp to datetime dtype
df_v1['timestamp'] = pd.to_datetime(df_v1['timestamp'], dayfirst=True)

#%%
# filter data so that the latest timestamp is the same for both old and new datasets
df_v2 = df_v2[df_v2.timestamp <= '2017-04-30 23:50:00.000']

#%%
df_v2.rename(columns = {'turbine_id': 'turbine'}, inplace=True) # rename columns 
df_v2.rename(columns = {'rs_av': 'rs_av_new'}, inplace=True)

#%%
df_v2 = df_v2.sort_values(['timestamp', 'turbine']) # sort values and drop duplicates
df_v1 = df_v1.sort_values(['timestamp', 'turbine'])
df_v2 = df_v2.drop_duplicates(['timestamp', 'turbine'], keep='first')
df_v1 = df_v1.drop_duplicates(['timestamp', 'turbine'], keep='first')

#%%
tmstmp = list(pd.date_range('2014-11-01 00:00:00', '2017-04-30 23:50:00', freq='10min')) # fill missing rows in time series
trbn = range(1, 26) # 1 to 25, for each of the 25 turbines
newcols = list(itertools.product(tmstmp, trbn))
df_cols = pd.DataFrame(newcols)
df_cols.columns = ['timestamp', 'turbine']
df_v2['ap_max'] = df_v2['ap_max'].astype(np.float64)
df_v1_cols = pd.merge(df_v1, df_cols, on=['timestamp', 'turbine'], how='outer')
del df_v1, df_cols

#%%
# merge old and new data by these columns
df_scada = pd.merge(df_v1_cols, df_v2, on=[
    'timestamp', 'turbine', 'ws_av', 'wd_av', 'ws_1', 'ws_2', 'wd_1', 'wd_2',
    'gen_sp', 'pitch', 'reactive_power', 'ap_max', 'ap_dev', 'ap_av',
    'nac_pos'], how='outer')
del df_v1_cols, df_v2

#%%
df_scada = df_scada.sort_values(['timestamp', 'turbine']) # sort and drop duplicates again
df_scada = df_scada.drop_duplicates(['timestamp', 'turbine'], keep='first')

#%%
def f_m2(c): # merge rotor speed readings
    if c['rs_av_new'] >= 0:
        return c['rs_av_new']
    else:
        return c['rs_av_old']
df_scada['rs_av'] = df_scada.apply(f_m2, axis=1)

#%%
df_scada = df_scada.drop('rs_av_old', axis=1) # drop old columns and reset index
df_scada = df_scada.drop('rs_av_new', axis=1)
df_scada.reset_index(drop=True, inplace=True)

#%% return dataframe columns and their dtypes
df_scada.dtypes

#%%
# return dataframe shape
df_scada.shape

#%%
df_scada.to_csv('data/SCADA_merged.csv', index=False) # write to new csv file
del df_scada