#%% [markdown]
# # Combining multiple csv files containing data into a single file

#%% [markdown]
# ## SCADA

#%%
# import libraries
import pandas as pd
import numpy as np
import itertools

#%%
# import data - versions 1 (old) and 2 (new)
scadaV11 = pd.read_csv(
    'data/Last_six_months_SCADA.csv', skip_blank_lines=True)
scadaV12 = pd.read_csv(
    'data/Prior_two_years_SCADA.csv', skip_blank_lines=True)
scadaV21 = pd.read_csv(
    'data/NS_SCADA_v2.csv', skip_blank_lines=True)
scadaV22 = pd.read_csv(
    'data/NS_SCADA_2017_v2.csv', skip_blank_lines=True)

#%%
# return columns and their dtypes for each dataframe
scadaV11.dtypes, scadaV12.dtypes, scadaV21.dtypes, scadaV22.dtypes

#%%
# return shapes of each dataframe
scadaV11.shape, scadaV12.shape, scadaV21.shape, scadaV22.shape

#%%
# rename ap_min in scadaV12 to ap_max
scadaV12.rename(columns={'ap_min': 'ap_max'}, inplace=True)

#%%
# fixing rotor speed readings due to errors in data
# define function to merge some old rotor speed readings with new data
def merge1(c):
    if c['turbine'] <= 20:
        return c['rs_av']
scadaV11['rs_av_old'] = scadaV11.apply(merge1, axis=1)
scadaV12['rs_av_old'] = scadaV12.apply(merge1, axis=1)

#%%
# delete original columns
scadaV11 = scadaV11.drop('rs_av', axis=1)
scadaV12 = scadaV12.drop('rs_av', axis=1)

#%%
# concatenate old and new scada files to one
scadaV1 = pd.concat([scadaV11, scadaV12])
scadaV2 = pd.concat([scadaV21, scadaV22])
# delete concatenated dataframes from memory
del scadaV11, scadaV12, scadaV21, scadaV22

#%%
# convert timestamp to datetime dtype
scadaV2['timestamp'] = pd.to_datetime(scadaV2['timestamp'])
scadaV1['timestamp'] = pd.to_datetime(scadaV1['timestamp'], dayfirst=True)

#%%
# filter data so that the latest timestamp is the same
# for both old and new datasets
scadaV2 = scadaV2[scadaV2.timestamp <= '2017-04-30 23:50:00.000']

#%%
# rename columns
scadaV2.rename(columns = {'turbine_id': 'turbine'}, inplace=True)
scadaV2.rename(columns = {'rs_av': 'rs_av_new'}, inplace=True)

#%%
# sort values and drop duplicates
scadaV2 = scadaV2.sort_values(['timestamp', 'turbine'])
scadaV1 = scadaV1.sort_values(['timestamp', 'turbine'])
scadaV2 = scadaV2.drop_duplicates(['timestamp', 'turbine'], keep='first')
scadaV1 = scadaV1.drop_duplicates(['timestamp', 'turbine'], keep='first')

#%%
# fill missing rows in time series
tmstmp = list(pd.date_range(
    '2014-11-01 00:00:00', '2017-04-30 23:50:00', freq='10min'))
# list of turbines -- 1 to 25, for each of the 25 turbines
trbn = range(1, 26)
newcols = list(itertools.product(tmstmp, trbn))
cols = pd.DataFrame(newcols)
cols.columns = ['timestamp', 'turbine']
scadaV2['ap_max'] = scadaV2['ap_max'].astype(np.float64)
scadaV1_cols = pd.merge(
    scadaV1, cols, on=['timestamp', 'turbine'], how='outer')
del scadaV1, cols

#%%
# merge old and new data by these columns
scada = pd.merge(scadaV1_cols, scadaV2, on=[
    'timestamp', 'turbine', 'ws_av', 'wd_av', 'ws_1', 'ws_2', 'wd_1',
    'wd_2', 'gen_sp', 'pitch', 'reactive_power', 'ap_max', 'ap_dev',
    'ap_av', 'nac_pos'], how='outer')
del scadaV1_cols, scadaV2

#%%
# sort and drop duplicates again
scada = scada.sort_values(['timestamp', 'turbine'])
scada = scada.drop_duplicates(['timestamp', 'turbine'], keep='first')

#%%
# merge rotor speed readings
def merge2(c):
    if c['rs_av_new'] >= 0:
        return c['rs_av_new']
    else:
        return c['rs_av_old']
scada['rs_av'] = scada.apply(merge2, axis=1)

#%%
# drop old columns and reset index
scada = scada.drop('rs_av_old', axis=1)
scada = scada.drop('rs_av_new', axis=1)
scada.reset_index(drop=True, inplace=True)

#%% return dataframe columns and their dtypes
scada.dtypes

#%%
# return dataframe shape
scada.shape

#%%
# write to new csv file
scada.to_csv('data/SCADA_merged.csv', index=False)
del scada
