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

# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Make a list of all the statistics we'll be looking at.
# These are all of the columns that we use for scoring in daily / weekly matchup.
stats = [
    'pts', 'min', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'ast', 'stl', 'tov', 'blk'
]

# There are two types of NBA fantasy leagues, but they take these statistics into consideration the same way.

# Read in files and clean them.
# We're going to use per season stats since they account for injury time outages better than per game.
csv = 'nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv'
df = pd.read_csv(
    csv, header=0
)

# Clean up data by dropping rows with missing values
df_cleaned = df.dropna(how='all')

# Remove outliers; rows of data that are going to skew averages.
# Specifically, we want to drop players who don't play much who are going to reduce our averages.
# print(df_cleaned['gp'].describe())

# Mean games played is 52.63 and std is 25.12. We can calculate the min games played to make it into model.
min_gp = df_cleaned['gp'].mean() - (df_cleaned['gp'].std() * 3)
# print(min_gp)

# Let's look at a graph of games played data and see if we can find a good cut-off
bin_value = np.arange(start=0, stop=82, step=2)
df_cleaned['gp'].hist(bins=bin_value, figsize=[14, 6])
# plt.show()

min_gp = 10
df_no_outliers = df_cleaned[df_cleaned['gp'] > min_gp]
# print(df_cleaned['player_id'].count(), df_filter['player_id'].count())

# Now it's time to normalize our data.
# Scoring 22 ppg in 1993 isn't the same as scoring 22 ppg in 2023. There have been more attempts and higher
# accuracy plus more adoption of three pointers, leading to more scoring. In order to compare across seasons,
# we need to normalize data to compare between decades. What we want is a funciton that factors min and max
# values from each season and normalizes all stats from all seasons.
# Let's normalize points in a new col. We're going to take the value, subtract the minumum value, and divide
# by difference between max and min values, and let's do it as a function.


def normalize_col(col):
    normalized_input = (col - col.min()) / (col.max() - col.min())
    return normalized_input

# Now let's iterate through all our stats and normalize them. We can do this as a function, too.


def normalize_df(df):
    for col in stats:
        df['{}_norm'.format(col)] = normalize_col(df[col])
    return df


# Finally, we need to do this for each season, which can be tricky to pick out the mean, min, and max for each season.
# Let's group by season_id and then run function.
df_normalized = grouped_df = df_no_outliers.groupby(
    ['season_id'], group_keys=True).apply(normalize_df)

# Now, we need to calculate player distance. This is also referred to as percent error, and shares how close players' 
# stats are. Our goal is to find the ten players with the shortest distance across all stats.
# We'll create a function called called calc_distance that takes two players as inputs and outputs their distance.
# To measure distance, we're going to use the euclidian distance between two points. This measures the length of the 
# distance between the two points. We can caluclate this with the square root function.


def calc_distance(u, v):
    dist = np.sqrt(np.sum((u - v) ** 2))
    return dist

# First we'll test two players and see how our function works. Let's join our df_normalized with a df
# with names to see names.
df_player_names = pd.read_csv('nbadata/nba-stats-csv/player_id_player_name.csv')
df_normalized = pd.merge(df_normalized, df_player_names, on = 'player_id', how='left')
col_list = df_normalized.columns.tolist()
col_list = col_list[0:1] + col_list[-1:] + col_list[1:-1]
df_normalized = df_normalized[col_list]

## Let's experiment by getting just Damien Lillard, Steph Curry, and The Stifle Tower in 2017-18
some_players_list = ['Steph Curry', 'Damian Lillard', 'Rudy Gobert']
dame_2019 = df_normalized[(df_normalized['player_name'] == 'Damian Lillard') & (df_normalized['season_id'] == '2018-19')] 
steph_2019 = df_normalized[(df_normalized['player_name'] == 'Stephen Curry') & (df_normalized['season_id'] == '2018-19')] 
stifle_2019 = df_normalized[(df_normalized['player_name'] == 'Rudy Gobert') & (df_normalized['season_id'] == '2018-19')] 
dame_2019_ppg = dame_2019.pts.tolist()[0]
steph_2019_ppg = steph_2019.pts.tolist()[0]
stifle_2019_ppg = stifle_2019.pts.tolist()[0]
print(calc_distance(dame_2019_ppg, steph_2019_ppg))