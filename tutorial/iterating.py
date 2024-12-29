## In our model, we'll need to loop over rows in dfs. When looping over
## df's there are two methods.
import pandas as pd
import numpy as np

nba_stats = {
    'first_name' : ['Lebron', 'Kyle', 'Lonzo', 'Brandon', 'Josh', 'Lance', 'Michael', 'Tyson', 'Ivica'],
    'last_name' : ['James', 'Kuzma', 'Ball', 'Ingram', 'Hart', 'Stephenson', 'Beasley', 'Chandler', 'Zubac'],
    'ppg' : [28.2, 21.1, 14.3, 17.2, 18.2, 11.2, 14.2, 4.5, 6.7],
    'apg' : [12.3,  2.1,  8.9,  2.5,  3.6,  0.2,  1.8, 1.9, 1.5],
    'rpg' : [ 7.1,  5.4,  5.5,  8.1,  3.2,  5.5,  7.7, 2.3, 8.1]
}
nba_stats_cols = ['first_name', 'last_name', 'ppg', 'apg', 'rpg']
laker_df = pd.DataFrame(nba_stats, columns=nba_stats_cols)
# print(laker_df)

## First we'll use the iterrows function. Pandas returns an iterator containing the index of each row
## and the data in each row as a series.
# for row in laker_df.iterrows():
#     print(row)

## Since each row is given as a series, we use the col name to access each col's val in row.
# for index, row in laker_df.iterrows():
    # print(row['first_name'], row['last_name'], row['ppg'])

## Second, itertuples function. This iterates through rows and returns row tuple. This is the preferred method.
## First row is index and rest is other column data in row. This is preferred because tuples are preferred to series.
# for row in laker_df.itertuples():
#     print(row.first_name, row.last_name, row.ppg)

## What if we want to iterate over df rows and take values and add them to an empty list:
ppg_data = []
for row in laker_df.itertuples():
    ppg_data.append(row.ppg)

print(ppg_data)