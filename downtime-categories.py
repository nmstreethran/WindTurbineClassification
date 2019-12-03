#%% [markdown]
# # Downtime frequency and period based on turbine category

#%%
# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%

df = pd.read_csv('data/turbine_categories.csv')
df['Turbine Category id'] = df['Turbine Category id'].astype(np.float64)
df = df.sort_values(by="freq/T/yr")
df['number'] = range(0, 23)
df.reset_index(drop=True, inplace=True)

#%%
y = df['number']
x1 = df['freq/T/yr']
x2 = df['period/T/yr']
list1 = df['Turbine Categories'].tolist()

#%%
fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(14, 7), dpi=500)
plt.suptitle('Turbine category', x=.513, y=.9, fontsize=12)
axes[0].barh(y, x1, align='center', color='#098A63')
axes[0].set_xlabel('Downtime frequency per turbine per year', fontsize=12)
axes[1].barh(y, x2, align='center', color='#3F2B78')
axes[1].set_xlabel('Downtime period (hours) per turbine per year', fontsize=12)

axes[0].invert_xaxis()
axes[0].set(yticks=y, yticklabels=list1)

axes[0].set(yticks=y, yticklabels=[])
for yloc, list1 in zip(y, list1):
    axes[0].annotate(list1, (.5, yloc), xycoords=('figure fraction', 'data'),
                     ha='center', va='center')

axes[0].yaxis.tick_right()

fig.subplots_adjust(wspace=.4, hspace=None)

plt.show()