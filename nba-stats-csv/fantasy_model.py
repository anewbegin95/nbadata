"""
This model will be inspired by a few things, including k nearest neighbors (KNN) and factor-adjusted team similarites (FATS) from NBA math.
We'll implement a manual model to find similar players.
Steps in this model:
    1. Normalize data acorss seasons
    2. Find the 10 most similar player seasons historically
    3. Rank and weight each of those 10 players season stats
    4. Look at 10 players following season's stats
    5. Use weighted averages to predict current players next season
    6. Rinse and repeat for every player in 2017 - 2018
Normalizing is crucial because averages change over time, and we want to know how similar players are to those averages. We want to look at
statistic strength compared to the league as a whole. Changes can be minor year-to-year, but very different over long spans of time.

To make things simple, we'll come up with one statistic called percent error to see how similar players are to each other. Meant to measure
distance in statistics between numbers. Only distance will matter in this comparison. We may not want to weight stats the same (i.e.: blocks
may not be weighted as highly as points)
"""

## Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Make a list of all the statistics we'll be looking at.
## These are all of the columns that we use for scoring in daily / weekly matchup.
stats = [
    'pts'
    ,'min'
    ,'fgm'
    ,'fga'
    ,'fg3m'
    ,'fg3a'
    ,'ftm'
    ,'fta'
    ,'oreb'
    ,'dreb'
    ,'ast'
    ,'stl'
    ,'tov'
    ,'blk'
]

## There are two types of NBA fantasy leagues, but they take these statistics into consideration the same way.

## Read in files and clean them.
## We're going to use per season stats since they account for injury time outages better than per game.
csv = 'nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv'
df = pd.read_csv(
    csv
    ,header = 0
    )

## Clean up data by dropping rows with missing values
df_cleaned = df.dropna(how='all')

## Remove outliers; rows of data that are going to skew averages. 
## Specifically, we want to drop players who don't play much who are going to reduce our averages.
# print(df_cleaned['gp'].describe())

## Mean games played is 52.63 and std is 25.12. We can calculate the min games played to make it into model.
min_gp = df_cleaned['gp'].mean() - (df_cleaned['gp'].std() * 3)
# print(min_gp)

## Let's look at a graph of games played data and see if we can find a good cut-off
bin_value = np.arange(start=0, stop=82, step=2)
df_cleaned['gp'].hist(bins=bin_value, figsize = [14,6])
# plt.show()

min_gp = 10
df_filter = df_cleaned[df_cleaned['gp'] > min_gp]
print(df_cleaned['player_id'].count(), df_filter['player_id'].count())