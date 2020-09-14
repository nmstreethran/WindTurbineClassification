"""Plot power vs. pitch angle for all turbines

"""

# import libraries
import pandas as pd
import itertools

# create dataframe from CSV
df = pd.read_csv('data/SCADA_merged.csv', skip_blank_lines=True)

# create pivot table (new dataframe)
power = pd.pivot_table(
    df, index=['ap_av'], columns=['turbine'], values=['pitch'])

# removing pivot table values name from heading
power.columns = power.columns.droplevel(0)

# list of column headers (i.e., turbines 1 to 25)
list1 = power.columns.tolist()

# create new list for individual subplot titles
list2 = [
    'Pitch angle vs. average active power for turbine %s' % x for x in list1]

# rename index
power.index.name = 'Average active power (kW)'

# plotting all columns (i.e., turbines 1 to 25) in the same figure
ax = power.plot(
    subplots=True, figsize=(50, 30), layout=(5, 5),
    style='.', sharex=False, title=list2, legend=False)
list3 = list(range(0, 5))
list4 = list(itertools.product(list3, list3))
for (x, y) in list4:
    ax[x][y].set_ylabel('Pitch angle (deg)')
