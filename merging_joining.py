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
raw_data_1 = {
    'player_id' : ['1', '2', '3', '4', '5', '6', '7']
    ,'first_name' : ['Lebron', 'Dirk', 'Vince', 'Enes', 'Derrick', 'Paul']
    ,'last_name' : ['James', 'Nowitzki', 'Carter', 'Kanter', 'Rose', 'George']
}