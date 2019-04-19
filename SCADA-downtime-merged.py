#%% [markdown]
# # Combining multiple csv files containing data into a single file

#%% [markdown]
# ## Merging SCADA and downtime

#%%
import pandas as pd # import libraries

#%%
# import downtime data
df_dwntm=pd.read_csv('DATA/downtime_merged.csv',skip_blank_lines=True)

#%%
df_dwntm['timestamp_start']=pd.to_datetime(df_dwntm['timestamp_start']) # convert dtype object to datetime
df_dwntm['timestamp_end']=pd.to_datetime(df_dwntm['timestamp_end'])

#%%
df_dwntm['timestamp_start']=df_dwntm['timestamp_start'].dt.round('10min') # round to nearest 10 min
df_dwntm['timestamp_end']=df_dwntm['timestamp_end'].dt.round('10min')

#%%
df_dwntm['period']=df_dwntm['timestamp_end']-df_dwntm['timestamp_start'] # calculate period

#%%
# downtime ranges to every ten minutes between start and end timestamps
df_dwntm=pd.concat([pd.DataFrame({'timestamp':pd.date_range(row.timestamp_start,row.timestamp_end,freq='10min'),
                             'turbine_id':row.turbine_id,'period':row.period,'TurbineCategory_id':row.TurbineCategory_id,
                             'EnvironmentalCategory_id':row.EnvironmentalCategory_id,
                             'InfrastructureCategory_id':row.InfrastructureCategory_id,
                             'GridCategory_id':row.GridCategory_id,
                             'AvailabilityCategory_id':row.AvailabilityCategory_id,'alarm_id':row.alarm_id,
                             'workorder_id':row.workorder_id,'comment':row.comment}, 
                            columns=['timestamp','turbine_id','period','TurbineCategory_id','EnvironmentalCategory_id',
                                     'InfrastructureCategory_id','GridCategory_id','AvailabilityCategory_id','alarm_id',
                                     'workorder_id','comment']) 
               for i,row in df_dwntm.iterrows()],ignore_index=True)

#%%
df_dwntm=df_dwntm.sort_values(['timestamp','turbine_id','period']) # sort and drop duplicates for same timestamp and turbine
df_dwntm=df_dwntm.drop_duplicates(['timestamp','turbine_id'],keep='first')

#%%
df_scada=pd.read_csv('DATA/SCADA_merged.csv',skip_blank_lines=True) # import SCADA 

#%%
df_scada=df_scada.drop('ws_1',axis=1) # drop unnecessary columns
df_scada=df_scada.drop('ws_2',axis=1)
df_scada=df_scada.drop('wd_1',axis=1)
df_scada=df_scada.drop('wd_2',axis=1)

#%%
df_scada['timestamp']=pd.to_datetime(df_scada['timestamp'],dayfirst=True) # convert timestamp to datetime

#%%
df_scada['turbine_id']=df_scada['turbine'] # copy turbine id to new column

#%%
df_merged=pd.merge(df_scada,df_dwntm,how='outer') # merge SCADA and downtime
del df_scada,df_dwntm

#%%
# drop downtime entries with no SCADA readings - in case of duplicates
df_merged=df_merged.drop(df_merged[(df_merged['turbine_id'].notnull())&(df_merged['turbine'].isnull())].index)

#%%
df_merged=df_merged.drop('turbine',axis=1) # drop old turbine id column

#%%
# list columns and their dtypes
df_merged.dtypes

#%% generate list of columns
list(df_merged.columns.values)

#%%
# rearrange columns
df_merged=df_merged[['timestamp',
 'turbine_id',
 'ap_av',
 'ap_dev',
 'ap_max',
 'reactive_power',
 'ws_av',
 'wd_av',
 'gen_sp',
 'nac_pos',
 'pitch',
 'rs_av',
 'runtime',
 'period',
 'TurbineCategory_id',
 'EnvironmentalCategory_id',
 'InfrastructureCategory_id',
 'GridCategory_id',
 'AvailabilityCategory_id',
 'alarm_id',
 'workorder_id',
 'comment']]

#%%
# write final dataframe to csv
df_merged.to_csv('DATA/SCADA_downtime_merged.csv',index=False)

#%%
# importing the new csv as a dataframe (encoding needs to be specified)
# import pandas as pd
# dfnew=pd.read_csv('DATA/SCADA_downtime_merged.csv',encoding="ISO-8859-1")