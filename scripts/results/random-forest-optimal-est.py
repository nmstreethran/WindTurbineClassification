"""Random forest classifier optimisation

"""

import numpy as np
import pandas as pd  # import libraries
from imblearn.over_sampling import RandomOverSampler
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import TimeSeriesSplit

# import data
df = pd.read_csv("data/SCADA_downtime_merged.csv", skip_blank_lines=True)

list1 = list(df["turbine_id"].unique())  # list of turbines to plot
list1 = sorted(list1, key=int)  # sort turbines in ascending order
list2 = list(df["TurbineCategory_id"].unique())  # list of categories
list2 = [g for g in list2 if g >= 0]  # remove NaN from list
list2 = sorted(list2, key=int)  # sort categories in ascending order
list2 = [m for m in list2 if m not in (1, 12, 13, 14, 15, 17, 21, 22)]
# categories to remove
list4 = list(range(0, 14))
list5 = list(zip(list4, list2))
e_p, e_r, e_f = [], [], []
# empty list to hold optimal n values for all turbines
pre, rec, f1s = [], [], []

for x in list1:  # filter only data for turbine x
    dfx = df[(df["turbine_id"] == x)].copy()
    for y in list2:
        # copying fault to new column (mins)
        # (fault when turbine category id is y)

        def ff(c):
            if c["TurbineCategory_id"] == y:
                return 0
            else:
                return 1

        dfx["mins"] = dfx.apply(ff, axis=1)

        dfx = dfx.sort_values(by="timestamp", ascending=False)
        # sort values by timestamp in descending order
        dfx.reset_index(drop=True, inplace=True)  # reset index

        if dfx.loc[0, "mins"] == 0:
            # assigning value to first cell if it's not 0
            dfx.set_value(0, "mins", 0)
        else:
            dfx.set_value(0, "mins", 999999999)

        for i, e in enumerate(dfx["mins"]):
            # using previous value's row to evaluate time
            if e == 1:
                dfx.at[i, "mins"] = dfx.at[i - 1, "mins"] + 10

        dfx = dfx.sort_values(by="timestamp")  # sort in ascending order
        dfx.reset_index(drop=True, inplace=True)  # reset index
        dfx["hours"] = dfx["mins"].astype(np.int64)
        # convert to hours, then round to nearest hour
        dfx["hours"] = dfx["hours"] / 60
        dfx["hours"] = round(dfx["hours"]).astype(np.int64)

        def f11(c):  # > 48 hours - label as normal (9999)
            if c["hours"] > 48:
                return 9999
            else:
                return c["hours"]

        dfx["hours"] = dfx.apply(f11, axis=1)

        def f22(
            c,
        ):
            # filter out curtailment - curtailed when turbine is pitching
            # outside 0 deg <= normal <= 3.5 deg
            if (
                0 <= c["pitch"] <= 3.5
                or c["hours"] != 9999
                or (
                    (c["pitch"] > 3.5 or c["pitch"] < 0)
                    and (
                        c["ap_av"] <= (0.1 * dfx["ap_av"].max())
                        or c["ap_av"] >= (0.9 * dfx["ap_av"].max())
                    )
                )
            ):
                return "normal"
            else:
                return "curtailed"

        dfx["curtailment"] = dfx.apply(f22, axis=1)

        def f3(
            c,
        ):
            # filter unusual readings, i.e., for normal operation,
            # power <= 0 in operating wind speeds, power > 100...
            # before cut-in, runtime < 600 and other downtime categories
            if c["hours"] == 9999 and (
                (
                    3 < c["ws_av"] < 25
                    and (
                        c["ap_av"] <= 0
                        or c["runtime"] < 600
                        or c["EnvironmentalCategory_id"] > 1
                        or c["GridCategory_id"] > 1
                        or c["InfrastructureCategory_id"] > 1
                        or c["AvailabilityCategory_id"] == 2
                        or 12 <= c["TurbineCategory_id"] <= 15
                        or 21 <= c["TurbineCategory_id"] <= 22
                    )
                )
                or (c["ws_av"] < 3 and c["ap_av"] > 100)
            ):
                return "unusual"
            else:
                return "normal"

        dfx["unusual"] = dfx.apply(f3, axis=1)

        def f4(c):  # round to 6 hour intervals
            if c["hours"] == 0:
                return 10
            elif 1 <= c["hours"] <= 6:
                return 11
            elif 7 <= c["hours"] <= 12:
                return 12
            elif 13 <= c["hours"] <= 18:
                return 13
            elif 19 <= c["hours"] <= 24:
                return 14
            elif 25 <= c["hours"] <= 30:
                return 15
            elif 31 <= c["hours"] <= 36:
                return 16
            elif 37 <= c["hours"] <= 42:
                return 17
            elif 43 <= c["hours"] <= 48:
                return 18
            else:
                return 19

        dfx["hours6"] = dfx.apply(f4, axis=1)

        def f5(c):  # change label for unusual and curtailed data (20)
            if c["unusual"] == "unusual" or c["curtailment"] == "curtailed":
                return 20
            else:
                return c["hours6"]

        dfx["hours_%s" % y] = dfx.apply(f5, axis=1)

        dfx = dfx.drop("hours6", axis=1)  # drop unnecessary columns
        dfx = dfx.drop("hours", axis=1)
        dfx = dfx.drop("mins", axis=1)
        dfx = dfx.drop("curtailment", axis=1)
        dfx = dfx.drop("unusual", axis=1)

    # separate features from classes for classification
    features = [
        "ap_av",
        "ws_av",
        "wd_av",
        "pitch",
        "ap_max",
        "ap_dev",
        "reactive_power",
        "rs_av",
        "gen_sp",
        "nac_pos",
    ]
    classes = [col for col in dfx.columns if "hours" in col]
    list6 = features + classes  # list of columns to copy into new df
    df2 = dfx[list6].copy()
    df2 = df2.dropna()  # drop NaNs
    X = df2[features]
    X = preprocessing.normalize(X)  # normalise features to values b/w 0 and 1
    Y = df2[classes]
    Y = Y.as_matrix()  # convert from pd dataframe to np array
    tscv = TimeSeriesSplit(n_splits=5)
    # cross validation using time series split
    myList = list(range(1, 100))
    # evaluating optimal number of trees
    # creating odd list of n
    est = list(filter(lambda x: x % 2 != 0, myList))
    # subsetting just the odd ones
    p, r, f = [], [], []

    for e in est:
        rf = RandomForestClassifier(criterion="entropy", n_jobs=-1, n_estimators=e)
        p1, r1, f1 = [], [], []
        for m, n in list5:
            Ym = Y[:, m]
            p2, r2, f2 = [], [], []
            for train_index, test_index in tscv.split(X):
                # looping for each cross validation fold
                X_train, X_test = (X[train_index], X[test_index])
                # split train and test sets
                Y_train, Y_test = Ym[train_index], Ym[test_index]
                if len(set(Y_train)) > 1:
                    ros = RandomOverSampler()
                    Xt, Yt = ros.fit_sample(X_train, Y_train)
                else:
                    Xt, Yt = X_train, Y_train
                rf1 = rf.fit(Xt, Yt)  # fit to classifier and predict
                Yp = rf1.predict(X_test)
                p_s = precision_score(Y_test[:, m], Yp[:, m], average="weighted")
                r_s = recall_score(Y_test[:, m], Yp[:, m], average="weighted")
                f_s = f1_score(Y_test[:, m], Yp[:, m], average="weighted")
                p2.append(p_s), r2.append(r_s), f2.append(f_s)
            p1.append(np.mean(p2)),
            r1.append(np.mean(r2)),
            f1.append(np.mean(f2))
        p.append(np.mean(p1)), r.append(np.mean(r1)), f.append(np.mean(f1))
    e_p.append(neighbours[p.index(max(p))]),
    e_r.append(neighbours[r.index(max(r))]),
    e_f.append(neighbours[f.index(max(f))])
    pre.append(max(p)),
    rec.append(max(r)),
    f1s.append(max(f))
    print("Classification report for turbine %s, turbine category %s" % (x, n))
    print(classification_report(Y_test, Yp, digits=6))
    print("----------------------------------------------------------------")
