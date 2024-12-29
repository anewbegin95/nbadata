## Pandas is like the baby of Excel and SQL. Most of the examples
## we've looked at so far align with Excel functions, but 
## concat / append will align more with SQL. We'll need to merge 
## frames when we pull from different sources. Concatenate and append
## are two of the most popular ways to merge data.

import pandas as pd

## Concat method is called directly on Pandas object, which is why
## we see "pd." directly before it. It will combine or concat
## two or more dataframes together and turn them into one dataframe.
## We can do this when df's have the same columns but different data.

## To learn about concat, set up two samples with the same cols
## but different records
df = pd.read_csv('nbadata/nba-stats-csv/nba_season_stats.csv')
df_a = df.sample(10)
df_b = df.sample(10)

## Concat takes just the two names as inputs. These can be fed as
## values directly or a list. Concat will stack the two dataframes
## on top of each other, like a UNION ALL in SQL.
# concat_list = [df_a, df_b]
# concat = pd.concat(concat_list)
# print(concat)

## You'll want to pay attention to indexes here. If you don't '
## explicity say what your index is, you can sometimes end up with
## duplicated index values. This can be an issue if you try to access
## rows by index. Example below:
raw_data_1 = {
    'player_id' : ['1', '2', '3', '4', '5']
    ,'ppg' : [14.5, 24.3, 28.3, 19.8, 29.2]
    ,'fg%' : [.57, .43, .38, .39, .57]
}
raw_data_2 = {
    'player_id' : ['6', '7', '8', '9', '10']
    ,'ppg' : [14.3, 22.3, 11.6, 10.6, 11.7]
    ,'fg%' : [.52, .48, .32, .37, .51]
}
df_1 = pd.DataFrame(raw_data_1, columns = ['player_id', 'ppg', 'fg%'])
df_2 = pd.DataFrame(raw_data_2, columns = ['player_id', 'ppg', 'fg%'])

sample_concat = pd.concat([df_1, df_2])
# print(sample_concat)

## Printing this will show that we've got default indicies on each
## data frame and that when we concatenated the dataframes, our 
## indicies are included since the ignore_index parameter is False by
## default. To override this we can set the default to True or reset 
## the index.
sample_concat = pd.concat([df_1, df_2], ignore_index=True)
# print(sample_concat)

## Earlier, we looked at the append method. This is the same, but
## it's called directly on a dataframe object. We don't call a list
## but call the command directly on the dataframe itself. Append has
## the same index issues that concat has, so be sure to reset your 
## index as needed.
appended = df_1.append(df_2, ignore_index = True)
print(appended)