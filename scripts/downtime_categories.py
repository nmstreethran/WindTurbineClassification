"""Downtime categories

Generating turbine downtime statistics
"""

import pandas as pd

data_cat = pd.read_csv("data/processed/downtime_categories.csv")
data_ts = pd.read_csv(
    "data/processed/downtime_timeseries.csv",
    lineterminator="\n",
    parse_dates=["timestamp_start", "timestamp_end"],
)

data_ts["period"] = data_ts["timestamp_end"] - data_ts["timestamp_start"]
data_ts["period"] = data_ts["period"].dt.total_seconds() / (60 * 60)

data = pd.DataFrame(data_ts.groupby(["TurbineCategory_id"]).count()["id"])
data.rename(columns={"id": "frequency"}, inplace=True)
data["Category"] = data.index

data["period"] = data_ts.groupby(["TurbineCategory_id"]).sum()["period"]

data["frequency/t/y"] = data["frequency"] / (25 * 2.5)
data["period/t/y"] = data["period"] / (25 * 2.5)

data_cat = data_cat[data_cat["Type"] == "Turbine"]
data_cat = data_cat.drop(columns=["Type"])

data = pd.concat([data, data_cat], axis=1)
data.fillna(0, inplace=True)
data.sort_values(by="frequency", inplace=True)

data.to_csv("data/processed/downtime_categories_stats.csv")
