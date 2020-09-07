"""Merging SCADA and downtime files

This script merges the SCADA and downtime merged datasets produced
in SCADA-merged.py and downtime-merged.py into a single CSV dataset.
Some unnecessary columns and duplicate data were dropped in the
process. The downtime categories act as labels for the SCADA data.
Therefore, this merging also automates the labelling process needed
to train classifiers for supervised learning.
"""

# import libraries
import pandas as pd

# import downtime data
dwntm = pd.read_csv('data/downtime_merged.csv', skip_blank_lines=True)

# convert data type object to datetime
dwntm['timestamp_start'] = pd.to_datetime(dwntm['timestamp_start'])
dwntm['timestamp_end'] = pd.to_datetime(dwntm['timestamp_end'])

# round to nearest 10 min
dwntm['timestamp_start'] = dwntm['timestamp_start'].dt.round('10min')
dwntm['timestamp_end'] = dwntm['timestamp_end'].dt.round('10min')

# calculate period
dwntm['period'] = dwntm['timestamp_end'] - dwntm['timestamp_start']

# downtime ranges to every ten minutes between start and end timestamps
dwntm = pd.concat([pd.DataFrame({
    'timestamp': pd.date_range(
        row.timestamp_start, row.timestamp_end, freq='10min'),
    'turbine_id': row.turbine_id,
    'period': row.period,
    'TurbineCategory_id': row.TurbineCategory_id,
    'EnvironmentalCategory_id': row.EnvironmentalCategory_id,
    'InfrastructureCategory_id': row.InfrastructureCategory_id,
    'GridCategory_id': row.GridCategory_id,
    'AvailabilityCategory_id': row.AvailabilityCategory_id,
    'alarm_id': row.alarm_id,
    'workorder_id': row.workorder_id,
    'comment': row.comment},
    columns=[
        'timestamp', 'turbine_id', 'period', 'TurbineCategory_id',
        'EnvironmentalCategory_id', 'InfrastructureCategory_id',
        'GridCategory_id', 'AvailabilityCategory_id', 'alarm_id',
        'workorder_id', 'comment'])
    for i, row in dwntm.iterrows()], ignore_index=True)

# sort and drop duplicates for same timestamp and turbine
dwntm = dwntm.sort_values(['timestamp', 'turbine_id', 'period'])
dwntm = dwntm.drop_duplicates(['timestamp', 'turbine_id'], keep='first')

# import SCADA
scada = pd.read_csv('data/SCADA_merged.csv', skip_blank_lines=True)

# drop unnecessary columns
scada = scada.drop(columns=['ws_1', 'ws_2', 'wd_1', 'wd_2'])

# convert timestamp to datetime
scada['timestamp'] = pd.to_datetime(scada['timestamp'], dayfirst=True)

# copy turbine ID to new column
scada['turbine_id'] = scada['turbine']

# merge SCADA and downtime
merged = pd.merge(scada, dwntm, how='outer')

# drop downtime entries with no SCADA readings - in case of duplicates
merged = merged.drop(
    merged[(
        merged['turbine_id'].notnull()) & (merged['turbine'].isnull())].index)

# drop old turbine ID column
merged = merged.drop('turbine', axis=1)

# rearrange columns
merged = merged[[
    'timestamp',
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

# write final dataframe to CSV
merged.to_csv('data/SCADA_downtime_merged.csv', index=False)
