# Inplace parameter used to overwrite original pandas object
# Oftentimes, this parameter is a dataframe
# The default setting is False, which is often why we see people use the same variable

import pandas as pd
df = pd.read_csv('nbadata/nba-stats-csv/player_stats_total.csv')

df_slim = df.sample(15)
df_slim.sort_values('gp')

# Printing the original df_slim set will ***NOT*** sort the dataset by games played
# like the code we wrote above says to do.
# print(df_slim)

# Unless we swap the values for the inplace parameter, we'll need to sort the 
# dataframe and save it to a new dataframe to get our sorted set.
df_slim_sorted = df_slim.sort_values('gp')
# print(df_slim_sorted)

# You can save your function to the **SAME** df to overwrite. However, this can be 
# confusing and isn't always the best way to do this.
df_slim = df.sample(15)
df_slim = df_slim.sort_values('gp')
# print(df_slim)

# Setting the inplace parameter to true will overwrite the dataframe to be sorted by 
# the field we've selected.
df_slim = df.sample(15)
df_slim.sort_values('gp', inplace = True)
print(df_slim)