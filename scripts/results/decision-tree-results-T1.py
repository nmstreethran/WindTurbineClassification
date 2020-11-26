"""Decision tree classifier results

"""

# import libraries
import subprocess
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import itertools
from sklearn import model_selection
from sklearn import preprocessing

# import data
df = pd.read_csv('data/SCADA_downtime_merged.csv', skip_blank_lines=True)

# list of turbines to plot
list1 = [1]
# list1 = list(df['turbine_id'].unique())
# sort turbines in ascending order
# list1 = sorted(list1, key=int)
# list of categories to plot
list2 = [11]
# list2 = list(df1['TurbineCategory_id'].unique())
# sort categories in ascending order
# list2 = sorted(list2, key=int)
# categories to remove from plot
# list2 = [e for e in list2 if e not in (1, 12, 13, 15, 21, 22)]
list3 = list(itertools.product(list1, list2))

for (x, y) in list3:
    # filter only data for turbine x
    dfx = df[(df['turbine_id'] == x)].copy()

    # sort values by timestamp in descending order
    dfx = dfx.sort_values(by='timestamp', ascending=False)

    # copying fault to new column (mins) (fault when turbine category id is y)
    def f(c):
        if c['TurbineCategory_id'] == y:
            return 0
        else:
            return 1
    dfx['mins'] = dfx.apply(f, axis=1)

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

    # convert to hours and round to nearest hour
    dfx['hours'] = dfx['mins'].astype(np.int64)
    dfx['hours'] = dfx['hours']/60
    dfx['hours'] = round(dfx['hours'])
    dfx['hours'] = dfx['hours'].astype(np.int64)

    # > 48 hours - label as normal (9999)
    def f1(c):
        if c['hours'] > 48:
            return 9999
        else:
            return c['hours']
    dfx['hours'] = dfx.apply(f1, axis=1)

    # filter out curtailment - curtailed when turbine is pitching outside
    # 0deg <= normal <= 3.5deg
    def f2(c):
        if 0 <= c['pitch'] <= 3.5 or c['hours'] != 9999 or (
            (c['pitch'] > 3.5 or c['pitch'] < 0) and (
                c['ap_av'] <= (.1 * dfx['ap_av'].max()) or
                c['ap_av'] >= (.9 * dfx['ap_av'].max()))):
            return 'normal'
        else:
            return 'curtailed'
    dfx['curtailment'] = dfx.apply(f2, axis=1)

    # filter unusual readings, i.e., for normal operation, power <= 0 in
    # operating wind speeds, power > 100 before cut-in, runtime < 600
    def f3(c):
        if c['hours'] == 9999 and ((
                3 < c['ws_av'] < 25 and (
                    c['ap_av'] <= 0 or c['runtime'] < 600 or
                    c['EnvironmentalCategory_id'] > 1 or
                    c['GridCategory_id'] > 1 or
                    c['InfrastructureCategory_id'] > 1 or
                    c['AvailabilityCategory_id'] == 2 or
                    12 <= c['TurbineCategory_id'] <= 15 or
                    21 <= c['TurbineCategory_id'] <= 22)) or
                (c['ws_av'] < 3 and c['ap_av'] > 100)):
            # remove unusual readings, i.e., zero power at operating wind
            # speeds, power > 0 before cut-in ...
            return 'unusual'
        else:
            return 'normal'
    dfx['unusual'] = dfx.apply(f3, axis=1)

    def f4(c):
        if 1 <= c['hours'] <= 6:
            return 6
        elif 7 <= c['hours'] <= 12:
            return 12
        elif 13 <= c['hours'] <= 18:
            return 18
        elif 19 <= c['hours'] <= 24:
            return 24
        elif 25 <= c['hours'] <= 30:
            return 30
        elif 31 <= c['hours'] <= 36:
            return 36
        elif 37 <= c['hours'] <= 42:
            return 42
        elif 43 <= c['hours'] <= 48:
            return 48
        else:
            return c['hours']
    dfx['hours6'] = dfx.apply(f4, axis=1)

    # filter data
    # normal w/o curtailment
    df3 = dfx[dfx.curtailment == 'normal']
    # normal w/o curtailment and unusual readings
    df3 = df3[df3.unusual == 'normal']

    df4 = df3[[
        'ap_av', 'ws_av', 'wd_av', 'pitch', 'ap_max', 'ap_dev',
        'reactive_power', 'rs_av', 'gen_sp', 'nac_pos', 'hours6']].copy()
    df4 = df4.dropna()

    # splitting data set
    features = [
        'ap_av', 'ws_av', 'wd_av', 'pitch', 'ap_max', 'ap_dev',
        'reactive_power', 'rs_av', 'gen_sp', 'nac_pos']
    X = df4[features]
    Y = df4['hours6']
    Xn = preprocessing.normalize(X)
    validation_size = .20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = (
        model_selection.train_test_split(
            Xn, Y, test_size=validation_size, random_state=seed))

    # fit using gini criterion
    clf = DecisionTreeClassifier(class_weight='balanced')
    clf = clf.fit(X_train, Y_train)

    predictions = clf.predict(X_validation)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

# after being fitted, the model can be used to predict the class of samples
clf.predict(X_validation)

# alternatively, the probability of each class can be predicted, which is the
# fraction of training samples of the same class in a leaf
clf.predict_proba(X_validation)

# using entropy
clf1 = DecisionTreeClassifier(criterion='entropy', class_weight='balanced')
clf1 = clf1.fit(X_train, Y_train)

predictions1 = clf1.predict(X_validation)
print(accuracy_score(Y_validation, predictions1))
print(confusion_matrix(Y_validation, predictions1))
print(classification_report(Y_validation, predictions1))

# fault
df4['fault'] = df4['hours6'].astype(str)


def fx(c):
    if c['fault'] == '9999':
        return 'normal'
    elif c['fault'] == '0':
        return 'faulty'
    else:
        return 'up to ' + c['fault'] + ' hr(s) before fault'


df4['fault'] = df4.apply(fx, axis=1)

# visualising


def visualise_tree(tree, feature_names):
    """Create tree svg using graphviz.

    Args
    ----
    tree -- scikit-learn DecisionTree.
    feature_names -- list of feature names.
    """
    with open('df.dot', 'w') as f:
        export_graphviz(
            tree, out_file=f, filled=True, rounded=True,
            feature_names=feature_names, special_characters=True,
            class_names=list(df4['fault'].unique()))

    command = ['dot', '-Tpng', 'df.dot', '-o', 'df.png']
    try:
        subprocess.check_call(command)
    except:
        exit('Could not run dot, i.e., graphviz, to produce visualisation')


visualise_tree(clf1, features)
