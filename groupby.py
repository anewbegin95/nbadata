## There might be a time we want to split the data into 
## groups and calculate summary statistics. This object
## is actually a different object than a pandas dataframe

## First, import libraries.
import pandas as pd
import numpy as np

## Next, get our traditional per game data.
df = pd.read_csv('nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv')

## Then, create a group by object.
groupby_df = df.groupby('season_id')

## Let's print the two types for these objects.
## Pandas is looping through and grouping all the objects
## into a single container dataframe that is a new groupby
## object.
# print(type(df))
# print(type(groupby))

## We can call specific methods on groupby objects. 
## Let's use our team data to see specific methods we 
## can run using player data.
df2 = pd.read_csv('nbadata/nba-stats-csv/nba_season_stats.csv')

## Let's group by team and see the mean age for each team.
teams = df2.groupby('Tm')
# teams = teams['Age'].mean().sort_values(ascending=False)
# print(teams)

## We can get info on specific groups as well using the getgroup 
## method.
celtics = teams.get_group('BOS')
# print(celtics)

## Let's now group by season id to see if points trend up over time
seasons = df.groupby('season_id')
total_points_by_season = seasons['pts'].sum()

## What if we want multiple metrics; can we get assists too?
total_pts_ast_by_season = seasons['pts', 'ast'].sum()
print(total_pts_ast_by_season)

## Groupby method follows split by / combine method.
## This means splitting data by a criteria and then grouping
## on some field and combining on another object.
## We can get summary statistics for each group we split on.
# print(type(seasons)) ##<class 'pandas.core.groupby.generic.DataFrameGroupBy'>

## We can apply the describe method to get even more statistics.
fg3m_describe = seasons['fg3m'].describe()
print(fg3m_describe)

## agg method; aggregation; helps perform operaitons on diff.
## columns. We could get the mean of one col and the sum of 
## another. 
seasons_agg = seasons.agg({
    'pts':'sum'
    ,'ast' : 'mean'
})
print(seasons_agg)