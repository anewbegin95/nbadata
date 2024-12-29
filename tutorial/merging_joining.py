## Joining / merging is another SQL thing where we bring two datasets 
## together and align them based on common columns. To merge in Pandas
## we use the merge method, which can be called on the df or pd object.
## Within the command we pass the left and right dataframes, the columns
## to join on, and the type of join we want to perform (left, right, etc.)

## First let's get our two datasets, one for player names and one with player data.
## The common column here is player id.
import pandas as pd
import numpy as np

stats_df = pd.read_csv('nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv')
player_name_df = pd.read_csv('nbadata/nba-stats-csv/player_id_player_name.csv')

# print(stats_df.head(10))
# print(player_name_df.head(10))

## When we merge these two, we'll see the player name on the right side.
merged_df = pd.merge(stats_df, player_name_df, on= 'player_id')
# print(merged_df.sample(10))

## If we only want to specify a few columns, we can do so in the command.
merged_df = pd.merge(
    player_name_df
    ,stats_df[['player_id', 'season_id', 'pts', 'ast', 'stl']]
    ,on= 'player_id'
)
# print(merged_df.sample(15))

## If you don't specify join type, you get inner join as a default.
## If you do this and you're missing data, it'll get dropped.
## We can run the same command and specify a join to get the same cols.
merged_df = pd.merge(
    player_name_df
    ,stats_df[['player_id', 'season_id', 'pts', 'ast', 'stl']]
    ,on= 'player_id'
    ,how='inner'
)
print(merged_df.sample(15))

## Let's explore more with some flubbed data
player_name_dict = {
    'player_id' : ['1', '2', '3', '4', '5', '6', '7']
    ,'first_name' : ['Lebron', 'Dirk', 'Vince', 'Enes', 'Fred', 'Derrick', 'Paul']
    ,'last_name' : ['James', 'Nowitzki', 'Carter', 'Kanter', 'Van Fleet', 'Rose', 'George']
}
player_career_ppg_dict = {
    'player_id' : ['1', '2', '3', '4', '5']
    ,'career_ppg' : [27.2, 20.7, 17.2, 11.9, 18.8]
}
player_name_df_2 = pd.DataFrame(
    player_name_dict
    ,columns= [
        'player_id'
        ,'first_name'
        ,'last_name'
    ]
)
player_career_ppg_df = pd.DataFrame(
    player_career_ppg_dict
    ,columns= [
        'player_id'
        ,'career_ppg'
    ]
)

## Left merge: just like an outer join. Keep all records
## in left dataframe and append any matching records in
## right dataframe based on "on" column. Any missing vals
## will result in NaN values.
left_merged_df = pd.merge(
    player_name_df_2
    ,player_career_ppg_df
    ,on='player_id'
    ,how='left'
)

## Because player_career_ppg_df doesn't have any values 
## for 6 or 7, those get NaN.
# print(left_merged_df)

## Right merge will do the same thing except it will
## keep all right df records and drop any non-matching
## left df records.
right_merged_df = pd.merge(
    player_name_df_2
    ,player_career_ppg_df
    ,on='player_id'
    ,how='right'
)

## This merge ony shows records 1-5 since those are the 
## only records in the right df.
# print(right_merged_df)

## We can do an outer merge which will produce all records
## and return NaN for anything with unmatched vals. Results
## here will be similar to left merge we did previously.
outer_merged_df = pd.merge(
    player_name_df_2
    ,player_career_ppg_df
    ,on='player_id'
    ,how='outer'
)
print(outer_merged_df)

## What if the keys we're joining on between tables are 
## different? Merge method can take left_on and right_on
## arguments to handle these situations.
## Let's get some more dummy data with mismatched key names.
player_name_dict_2 = {
    'id' : ['1', '2', '3', '4', '5', '6', '7']
    ,'first_name' : ['Lebron', 'Dirk', 'Vince', 'Enes', 'Fred', 'Derrick', 'Paul']
    ,'last_name' : ['James', 'Nowitzki', 'Carter', 'Kanter', 'Van Fleet', 'Rose', 'George']
}
player_career_ppg_dict_2 = {
    'player_id' : ['1', '2', '3', '4', '5']
    ,'career_ppg' : [27.2, 20.7, 17.2, 11.9, 18.8]
}
player_name_df_3 = pd.DataFrame(
    player_name_dict_2
    ,columns= [
        'id'
        ,'first_name'
        ,'last_name'
    ]
)
player_career_ppg_df_2 = pd.DataFrame(
    player_career_ppg_dict_2
    ,columns= [
        'player_id'
        ,'career_ppg'
    ]
)

## We can include the left / right on arguments to merge 
## these two dataframes.
mismatched_on_merge_df = pd.merge(
    player_name_df_3
    ,player_career_ppg_df_2
    ,how = 'right'
    ,left_on = 'id'
    ,right_on = 'player_id'
)

## This will produce our desired join but we also
## get both ID columns. 
# print(mismatched_on_merge_df)

## We can use the drop method to get rid of a
## column by passing the name and axis.
mismatched_on_merge_df = pd.merge(
    player_name_df_3
    ,player_career_ppg_df_2
    ,how = 'right'
    ,left_on = 'id'
    ,right_on = 'player_id'
).drop('id', axis=1)

print(mismatched_on_merge_df)

## We can also call a merge directly on a dataframe
## rather than calling the pandas object.
direct_left_merge = player_name_df_3.merge(
    player_career_ppg_df_2
    ,how='left'
    ,left_on = 'id'
    ,right_on = 'player_id'
    ).drop('id', axis=1)
print(direct_left_merge)