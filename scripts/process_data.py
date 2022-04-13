# %% [markdown]
# # Process data

# %% [markdown]
# ## Downtime categories

# %%
# import libraries
import os
import glob
import itertools
import pandas as pd
import numpy as np

# %%
# create directory to store processed data
os.makedirs("data/processed/", exist_ok=True)

# %%
# read and view data
data = pd.read_excel("data/Melogale Downtime Categories.xlsx")

# %%
# drop first row
data = data.drop([0])

# %%
# function to filter data for each category type
catData = {}


def categorise_data(cat, number):
    catData[cat] = data.filter(
        items=[cat+" Categories", "Unnamed: "+str(number)]
    )
    catData[cat].rename(
        columns={
            cat+" Categories": "Category", "Unnamed: "+str(number): "Name"
        },
        inplace=True
    )
    catData[cat]["Type"] = cat
    catData[cat].dropna(inplace=True)


# %%
# filtering
categorise_data("Turbine", 1)
categorise_data("Environmental", 3)
categorise_data("Grid", 5)
categorise_data("Infrastructure", 7)
categorise_data("Availability", 9)

# %%
# concatenate data
data = pd.concat(catData.values(), ignore_index=True)

# %%
# save data as CSV
data.to_csv("data/processed/downtime_categories.csv", index=False)

# %% [markdown]
# ## Downtime time series

# %%
dt = {}
dtList = glob.glob("data/*downtime*.csv")
for num, df in enumerate(dtList):
    dt[num] = pd.read_csv(df)
    print(num, df, dt[num].shape)

# %%
# drop duplicate columns
dt[1].drop(columns=list(dt[1].filter(regex=".1")), inplace=True)

# %%
# convert timestamps to datetime data type
for key in dt.keys():
    for col in list(dt[key].filter(regex="timestamp")):
        dt[key][col] = pd.to_datetime(dt[key][col])

# %%
# concatenate data
data = pd.concat(dt.values(), join="outer")

# %%
# sort by timestamp, then by turbine
data = data.sort_values(["timestamp_start", "timestamp_end", "turbine_id"])

# %%
# reset index after sort
data.reset_index(drop=True, inplace=True)

# %%
# save dataframe as new CSV
data.to_csv(
    "data/processed/downtime_timeseries.csv", index=False, encoding="utf-8"
)

# %% [markdown]
# ## SCADA time series

# %%
# old SCADA data
scada = {}
scadaList = glob.glob("data/*SCADA.csv")
for num, df in enumerate(scadaList):
    scada[num] = pd.read_csv(df)
    print(num, df, scada[num].shape)

# %%
# rename ap_min in scada[1] to ap_max
scada[1].rename(columns={"ap_min": "ap_max"}, inplace=True)


# %%
# fixing rotor speed readings due to errors in data
def fix_rs(c):
    if c["turbine"] <= 20:
        return c["rs_av"]


# %%
for df in scada.keys():
    scada[df]["rs_av_old"] = scada[df].apply(fix_rs, axis=1)
    scada[df] = scada[df].drop("rs_av", axis=1)

# %%
# concatenate old datasets
scadaOld = pd.concat(scada.values())

# %%
# new SCADA data
scada = {}
scadaList = glob.glob("data/NS_SCADA*.csv")
for num, df in enumerate(scadaList):
    scada[num] = pd.read_csv(df)
    print(num, df, scada[num].shape)

# %%
# concatenate new datasets
scadaNew = pd.concat(scada.values())

# %%
# convert timestamp to datetime data type
scadaNew["timestamp"] = pd.to_datetime(scadaNew["timestamp"])
scadaOld["timestamp"] = pd.to_datetime(scadaOld["timestamp"], dayfirst=True)

# %%
# rename columns
scadaNew.rename(columns={"turbine_id": "turbine"}, inplace=True)
scadaNew.rename(columns={"rs_av": "rs_av_new"}, inplace=True)

# %%
# sort values and drop duplicates
scadaNew = scadaNew.sort_values(["timestamp", "turbine"])
scadaOld = scadaOld.sort_values(["timestamp", "turbine"])
scadaNew = scadaNew.drop_duplicates(["timestamp", "turbine"], keep="first")
scadaOld = scadaOld.drop_duplicates(["timestamp", "turbine"], keep="first")

# %%
# fill missing rows in time series
tmstmp = list(pd.date_range(
    "2014-11-01 00:00:00", "2017-04-30 23:50:00", freq="10min"
))

# list of turbines -- 1 to 25, for each of the 25 turbines
trbn = range(1, 26)

newcols = list(itertools.product(tmstmp, trbn))
cols = pd.DataFrame(newcols)
cols.columns = ["timestamp", "turbine"]
scadaNew["ap_max"] = scadaNew["ap_max"].astype(np.float64)
scadaOld_cols = pd.merge(
    scadaOld, cols, on=["timestamp", "turbine"], how="outer"
)

# %%
# merge old and new data by these columns
scada = pd.merge(scadaOld_cols, scadaNew, on=[
    "timestamp", "turbine", "ws_av", "wd_av", "ws_1", "ws_2", "wd_1",
    "wd_2", "gen_sp", "pitch", "reactive_power", "ap_max", "ap_dev",
    "ap_av", "nac_pos"
], how="outer")

# %%
# sort and drop duplicates again
scada = scada.sort_values(["timestamp", "turbine"])
scada = scada.drop_duplicates(["timestamp", "turbine"], keep="first")


# %%
# merge rotor speed readings
def merge_rotor_readings(c):
    if c["rs_av_new"] >= 0:
        return c["rs_av_new"]
    else:
        return c["rs_av_old"]


scada["rs_av"] = scada.apply(merge_rotor_readings, axis=1)

# %%
# drop old columns and reset index
scada = scada.drop("rs_av_old", axis=1)
scada = scada.drop("rs_av_new", axis=1)
scada.reset_index(drop=True, inplace=True)

# %%
# write to new CSV file
scada.to_csv("data/processed/SCADA_timeseries.csv", index=False)
