"""Plots of results

"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# decision trees
d = pd.read_csv('data/DT.csv')

# per turbine
d0 = d.groupby('turbine', as_index=False)['f1'].mean()
d1 = d.groupby('turbine', as_index=False)['f1'].max()
d2 = d.groupby('turbine', as_index=False)['f1'].min()
d3 = d.groupby('turbine', as_index=False)['f'].mean()
d4 = d.groupby('turbine', as_index=False)['f'].max()
d5 = d.groupby('turbine', as_index=False)['f'].min()

x = np.array(d0['turbine'])
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(list(range(1, 26)))
plt.xlabel('Turbine')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# per turbine category
d0 = d.groupby('fault', as_index=False)['f1'].mean()
d1 = d.groupby('fault', as_index=False)['f1'].max()
d2 = d.groupby('fault', as_index=False)['f1'].min()
d3 = d.groupby('fault', as_index=False)['f'].mean()
d4 = d.groupby('fault', as_index=False)['f'].max()
d5 = d.groupby('fault', as_index=False)['f'].min()

x = np.array(list(range(1, 15)))
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(range(1, 15), sorted(d0['fault'].tolist(), key=int))
plt.xlabel('Turbine category')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# random forests
d = pd.read_csv('data/RF.csv')

# per turbine
d0 = d.groupby('turbine', as_index=False)['f1'].mean()
d1 = d.groupby('turbine', as_index=False)['f1'].max()
d2 = d.groupby('turbine', as_index=False)['f1'].min()
d3 = d.groupby('turbine', as_index=False)['f'].mean()
d4 = d.groupby('turbine', as_index=False)['f'].max()
d5 = d.groupby('turbine', as_index=False)['f'].min()

x = np.array(d0['turbine'])
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(list(range(1, 26)))
plt.xlabel('Turbine')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# per turbine category
d0 = d.groupby('fault', as_index=False)['f1'].mean()
d1 = d.groupby('fault', as_index=False)['f1'].max()
d2 = d.groupby('fault', as_index=False)['f1'].min()
d3 = d.groupby('fault', as_index=False)['f'].mean()
d4 = d.groupby('fault', as_index=False)['f'].max()
d5 = d.groupby('fault', as_index=False)['f'].min()

x = np.array(list(range(1, 15)))
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(range(1, 15), sorted(d0['fault'].tolist(), key=int))
plt.xlabel('Turbine category')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# k nearest neighbours
d = pd.read_csv('data/knn.csv')

# per turbine
d0 = d.groupby('turbine', as_index=False)['f1'].mean()
d1 = d.groupby('turbine', as_index=False)['f1'].max()
d2 = d.groupby('turbine', as_index=False)['f1'].min()
d3 = d.groupby('turbine', as_index=False)['f'].mean()
d4 = d.groupby('turbine', as_index=False)['f'].max()
d5 = d.groupby('turbine', as_index=False)['f'].min()

x = np.array(d0['turbine'])
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(list(range(1, 26)))
plt.xlabel('Turbine')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# per turbine category
d0 = d.groupby('fault', as_index=False)['f1'].mean()
d1 = d.groupby('fault', as_index=False)['f1'].max()
d2 = d.groupby('fault', as_index=False)['f1'].min()
d3 = d.groupby('fault', as_index=False)['f'].mean()
d4 = d.groupby('fault', as_index=False)['f'].max()
d5 = d.groupby('fault', as_index=False)['f'].min()

x = np.array(list(range(1, 15)))
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='#3F2B78', marker='o', label='imbalanced')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None',
    ecolor='#3F2B78', capsize=3)
plt.xticks(range(1, 15), sorted(d0['fault'].tolist(), key=int))
plt.xlabel('Turbine category')
plt.ylabel('F1 score')
plt.legend(loc=4)
plt.show()

# kNN optimised k
d_k = pd.read_csv('data/knn-k.csv')

# per turbine
d0 = d_k.groupby('turbine', as_index=False)['f1'].mean()
d1 = d_k.groupby('turbine', as_index=False)['f1'].max()
d2 = d_k.groupby('turbine', as_index=False)['f1'].min()
d3 = d_k.groupby('turbine', as_index=False)['f'].mean()
d4 = d_k.groupby('turbine', as_index=False)['f'].max()
d5 = d_k.groupby('turbine', as_index=False)['f'].min()

x = np.array(d0['turbine'])
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

d6 = d.groupby('turbine', as_index=False)['f1'].mean()
d7 = d.groupby('turbine', as_index=False)['f1'].max()
d8 = d.groupby('turbine', as_index=False)['f1'].min()
y2 = np.array(d6['f1'])
eh2 = np.array(d7['f1'])
el2 = np.array(d8['f1'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y2, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y2, [y2 - el2, eh2 - y2], linestyle='None',
    ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y, linestyle='None', color='#3F2B78',
    marker='o', label='imbalanced, without k optimisation')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#3F2B78', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='C0', marker='o',
    label='imbalanced, with k optimisation')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None', ecolor='C0', capsize=3)
plt.xticks(list(range(1, 26)))
plt.xlabel('Turbine')
plt.ylabel('F1 score')
plt.legend()
plt.show()

# per turbine category
d0 = d_k.groupby('fault', as_index=False)['f1'].mean()
d1 = d_k.groupby('fault', as_index=False)['f1'].max()
d2 = d_k.groupby('fault', as_index=False)['f1'].min()
d3 = d_k.groupby('fault', as_index=False)['f'].mean()
d4 = d_k.groupby('fault', as_index=False)['f'].max()
d5 = d_k.groupby('fault', as_index=False)['f'].min()

d6 = d.groupby('fault', as_index=False)['f1'].mean()
d7 = d.groupby('fault', as_index=False)['f1'].max()
d8 = d.groupby('fault', as_index=False)['f1'].min()
y2 = np.array(d6['f1'])
eh2 = np.array(d7['f1'])
el2 = np.array(d8['f1'])

x = np.array(list(range(1, 15)))
y = np.array(d0['f1'])
eh = np.array(d1['f1'])
el = np.array(d2['f1'])
y1 = np.array(d3['f'])
eh1 = np.array(d4['f'])
el1 = np.array(d5['f'])

fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.errorbar(
    x, y2, linestyle='None', color='#098A63', marker='o', label='balanced')
plt.errorbar(
    x, y2, [y2 - el2, eh2 - y2], linestyle='None',
    ecolor='#098A63', capsize=3)
plt.errorbar(
    x, y, linestyle='None', color='#3F2B78',
    marker='o', label='imbalanced, without k optimisation')
plt.errorbar(
    x, y, [y - el, eh - y], linestyle='None', ecolor='#3F2B78', capsize=3)
plt.errorbar(
    x, y1, linestyle='None', color='C0', marker='o',
    label='imbalanced, with k optimisation')
plt.errorbar(
    x, y1, [y1 - el1, eh1 - y1], linestyle='None', ecolor='C0', capsize=3)
plt.xticks(range(1, 15), sorted(d0['fault'].tolist(), key=int))
plt.xlabel('Turbine category')
plt.ylabel('F1 score')
plt.legend()
plt.show()

# optimal k
d = pd.read_csv('data/knn-optimal.csv')
x = d['turbine']
y = d['k_p']
y1 = d['k_r']
y2 = d['k_f']
fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.plot(x, y, color='c', label='k_precision', marker='o')
plt.plot(x, y1, color='#098A63', label='k_recall', marker='o')
plt.plot(x, y2, color='#3F2B78', label='k_F1-score', marker='o')
plt.xlabel('Turbine')
plt.ylabel('Optimal k value')
plt.xticks(range(1, 26))
plt.legend()
plt.show()

# optimal k - F1 score
fig, ax = plt.subplots(figsize=(10, 4), dpi=500)
plt.plot(x, y2, color='#3F2B78', label='k_F1-score', marker='o')
plt.xlabel('Turbine')
plt.ylabel('Optimal k value')
plt.xticks(range(1, 26))
plt.show()
