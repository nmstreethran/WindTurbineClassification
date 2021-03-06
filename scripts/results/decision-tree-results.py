"""Results for decision tree classifier

"""

# import libraries
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report
from imblearn.over_sampling import RandomOverSampler

# import data
df = pd.read_csv('data/SCADA_downtime_merged.csv', skip_blank_lines=True)

# list of turbines to plot
list1 = list(df['turbine_id'].unique())
# sort turbines in ascending order
list1 = sorted(list1, key=int)
# list of categories
list2 = list(df['TurbineCategory_id'].unique())
# remove NaN from list
list2 = [g for g in list2 if g >= 0]
# sort categories in ascending order
list2 = sorted(list2, key=int)
# categories to remove
list2 = [m for m in list2 if m not in (1, 12, 13, 14, 15, 17, 21, 22)]
list4 = list(range(0, 14))
list5 = list(zip(list4, list2))

# filter only data for turbine x
for x in list1:
    dfx = df[(df['turbine_id'] == x)].copy()
    # copying fault to new column (mins) (fault when turbine category id is y)
    for y in list2:
        def ff(c):
            if c['TurbineCategory_id'] == y:
                return 0
            else:
                return 1
        dfx['mins'] = dfx.apply(ff, axis=1)

        # sort values by timestamp in descending order
        dfx = dfx.sort_values(by='timestamp', ascending=False)
        # reset index
        dfx.reset_index(drop=True, inplace=True)

        # assigning value to first cell if it's not 0
        if dfx.loc[0, 'mins'] == 0:
            dfx.set_value(0, 'mins', 0)
        else:
            dfx.set_value(0, 'mins', 999999999)

        # using previous value's row to evaluate time
        for i, e in enumerate(dfx['mins']):
            if e == 1:
                dfx.at[i, 'mins'] = dfx.at[i-1, 'mins'] + 10

        # sort in ascending order
        dfx = dfx.sort_values(by='timestamp')
        # reset index
        dfx.reset_index(drop=True, inplace=True)
        # convert to hours, then round to nearest hour
        dfx['hours'] = dfx['mins'].astype(np.int64)
        dfx['hours'] = dfx['hours']/60
        dfx['hours'] = round(dfx['hours']).astype(np.int64)

        # > 48 hours - label as normal (9999)
        def f11(c):
            if c['hours'] > 48:
                return 9999
            else:
                return c['hours']
        dfx['hours'] = dfx.apply(f11, axis=1)

        # filter out curtailment - curtailed when turbine is pitching outside
        # 0 deg <= normal <= 3.5 deg
        def f22(c):
            if 0 <= c['pitch'] <= 3.5 or c['hours'] != 9999 or (
                    (c['pitch'] > 3.5 or c['pitch'] < 0) and (
                        c['ap_av'] <= (.1 * dfx['ap_av'].max())
                        or c['ap_av'] >= (.9*dfx['ap_av'].max()))):
                return 'normal'
            else:
                return 'curtailed'
        dfx['curtailment'] = dfx.apply(f22, axis=1)

        # filter unusual readings, i.e., for normal operation, power <= 0
        # in operating wind speeds, power > 100...
        # before cut-in, runtime < 600 and other downtime categories
        def f3(c):
            if c['hours'] == 9999 and ((
                        3 < c['ws_av'] < 25 and (
                            c['ap_av'] <= 0 or
                            c['runtime'] < 600 or
                            c['EnvironmentalCategory_id'] > 1 or
                            c['GridCategory_id'] > 1 or
                            c['InfrastructureCategory_id'] > 1 or
                            c['AvailabilityCategory_id'] == 2 or
                            12 <= c['TurbineCategory_id'] <= 15 or
                            21 <= c['TurbineCategory_id'] <= 22)) or
                    (c['ws_av'] < 3 and c['ap_av'] > 100)):
                return 'unusual'
            else:
                return 'normal'
        dfx['unusual'] = dfx.apply(f3, axis=1)

        # round to 6 hour intervals
        def f4(c):
            if c['hours'] == 0:
                return 10
            elif 1 <= c['hours'] <= 6:
                return 11
            elif 7 <= c['hours'] <= 12:
                return 12
            elif 13 <= c['hours'] <= 18:
                return 13
            elif 19 <= c['hours'] <= 24:
                return 14
            elif 25 <= c['hours'] <= 30:
                return 15
            elif 31 <= c['hours'] <= 36:
                return 16
            elif 37 <= c['hours'] <= 42:
                return 17
            elif 43 <= c['hours'] <= 48:
                return 18
            else:
                # normal
                return 19
        dfx['hours6'] = dfx.apply(f4, axis=1)

        # change label for unusual and curtailed data (20)
        def f5(c):
            if c['unusual'] == 'unusual' or c['curtailment'] == 'curtailed':
                return 20
            else:
                return c['hours6']
        dfx['hours_%s' % y] = dfx.apply(f5, axis=1)

        # drop unnecessary columns
        dfx = dfx.drop('hours6', axis=1)
        dfx = dfx.drop('hours', axis=1)
        dfx = dfx.drop('mins', axis=1)
        dfx = dfx.drop('curtailment', axis=1)
        dfx = dfx.drop('unusual', axis=1)

    # separate features from classes for classification
    features = [
        'ap_av', 'ws_av', 'wd_av', 'pitch', 'ap_max', 'ap_dev',
        'reactive_power', 'rs_av', 'gen_sp', 'nac_pos']
    classes = [col for col in dfx.columns if 'hours' in col]
    # list of columns to copy into new df
    list6 = features + classes
    df2 = dfx[list6].copy()
    # drop NaNs
    df2 = df2.dropna()
    X = df2[features]
    # normalise features to values b/w 0 and 1
    X = preprocessing.normalize(X)
    Y = df2[classes]
    # convert from pd dataframe to np array
    Y = Y.as_matrix()
    # cross validation using time series split
    tscv = TimeSeriesSplit(n_splits=5)

    dt = DecisionTreeClassifier(criterion='entropy')
    for (m, n) in list5:
        Ym = Y[:, m]
        # looping for each cross validation fold
        for train_index, test_index in tscv.split(X):
            # split train and test sets
            X_train, X_test = X[train_index], X[test_index]
            Y_train, Y_test = Ym[train_index], Ym[test_index]
            if len(set(Y_train)) > 1:
                ros = RandomOverSampler()
                Xt, Yt = ros.fit_sample(X_train, Y_train)
            else:
                Xt, Yt = X_train, Y_train
            # fit to classifier and predict
            dt1 = dt.fit(Xt, Yt)
            Yp = dt1.predict(X_test)
            print(
                'Classification report for turbine %s, turbine category %s'
                % (x, n))
            print(classification_report(Y_test, Yp, digits=6))
        print('-------------------------------------------------------------')
