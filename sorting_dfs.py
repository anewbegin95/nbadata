import pandas as pd
import numpy as np

## First, let's sort by index. 
## We'll use the lakers_dict dictionary we created earlier.
lakers_dict = {
    'first_name' : ['Lebron', 'Kyle', 'Lonzo', 'Brandon', 'Lance', 'Josh', 'Michael', 'Tyson'],
    'last_name' : ['James', 'Kuzma', 'Ball', 'Ingram', 'Stephenson','Hart', 'Beasley', 'Chandler'],
    'ppg' : [27.4, 18.7, 9.9, 18.3, 7.2, 7.8, 7.0, 3.1],
    'apg' : [8.3, 2.5, 5.4, 3.0, 2.1, 1.4, 1.0, 0.6,],
    'rpg' : [8.5, 5.5, 5.3, 5.1, 3.2, 3.7, 2.3, 5.6]
}

## Create a dataframe (unsorted_df) with all of the indicies out of order.
unsorted_df = pd.DataFrame(lakers_dict, index=[1,3,6,2,3,5,0,7])

## Printing said dataframe will reveal that index isn't sorted numerically.
# print(unsorted_df)

## We can use the sort index method to sort the index.
## Rows will be rearranged by index number now
sorted_df = unsorted_df.sort_index()
# print(sorted_df)

## We can sort values in a dataframe with a different sort method.
## This sort is, by default, ascending (low to high).
## Setting the parameter ascending=False, we'll get descending vals (high to low).
pts_sorted_df = sorted_df.sort_values('ppg', ascending=False)
# print(pts_sorted_df)

## If you want to sort on multiple values, pass in a list of fields
multi_sorted_df = unsorted_df.sort_values(['ppg', 'apg'], ascending=False)

print(multi_sorted_df)

## There are times when datasets will have nulls. To make these easy to identify,
## you may want to put the null values at the top or bottom of the dataset.
## To handle this, we'll pass a new argument to handle these values.
## First, let's create a new dictionary with null values using np.nan.
lakers_dict_with_nulls = {
    'first_name' : ['Lebron', 'Kyle', 'Lonzo', 'Brandon', 'Lance', 'Josh', 'Michael', 'Tyson'],
    'last_name' : ['James', 'Kuzma', 'Ball', 'Ingram', 'Stephenson','Hart', 'Beasley', 'Chandler'],
    'ppg' : [27.4, 18.7, np.nan, 18.3, np.nan, 7.8, 7.0, 3.1],
    'apg' : [8.3, 2.5, 5.4, 3.0, 2.1, 1.4, 1.0, 0.6,],
    'rpg' : [8.5, 5.5, 5.3, 5.1, 3.2, 3.7, 2.3, 5.6]
}

df_with_nulls = pd.DataFrame(lakers_dict_with_nulls)

## Using the na_position argument, we can pass a string to put the nulls first or last.
df_with_nulls.sort_values('ppg', inplace=True, ascending=False, na_position='first')
# print(df_with_nulls)