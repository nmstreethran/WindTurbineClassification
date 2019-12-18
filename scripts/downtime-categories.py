#%% [markdown]
# # Plotting downtime frequency and period based on the turbine category

#%%
"""Plotting downtime frequency and period based on the turbine category

"""

#%%
# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
# read turbine categories data
tc = pd.read_csv('data/turbine_categories.csv')
# convert category id to float
tc['Turbine Category id'] = tc['Turbine Category id'].astype(np.float64)
# sort by frequency of category / turbine / year
tc = tc.sort_values(by='freq/T/yr')
# list of numbers for each category id
tc['number'] = range(0, 23)
# reset index
tc.reset_index(drop=True, inplace=True)
tc

#%%
# set axes and list categories
y = tc['number']
x1 = tc['freq/T/yr']
x2 = tc['period/T/yr']
cat = tc['Turbine Categories'].tolist()

#%%
# create bar chart with shared y axis and two columns
# specifying figure dimensions and resolution
fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(14, 7), dpi=500)
plt.suptitle('Turbine category', x=.513, y=.9, fontsize=12)

#%%
# first column -- downtime frequency per turbine per year
axes[0].barh(y, x1, align='center', color='#098A63')
axes[0].set_xlabel(
    'Downtime frequency per turbine per year', fontsize=12)

#%%
# second column -- downtime period per turbine per year
axes[1].barh(y, x2, align='center', color='#3F2B78')
axes[1].set_xlabel(
    'Downtime period (hours) per turbine per year', fontsize=12)

#%%
# invert the x axis and set axis ticks and labels
axes[0].invert_xaxis()
axes[0].set(yticks=y, yticklabels=cat)
axes[0].set(yticks=y, yticklabels=[])
for yloc, cat in zip(y, cat):
    axes[0].annotate(cat, (.5, yloc), xycoords=(
        'figure fraction', 'data'), ha='center', va='center')
axes[0].yaxis.tick_right()

#%%
# create plot
fig.subplots_adjust(wspace=.4, hspace=None)
plt.show()
