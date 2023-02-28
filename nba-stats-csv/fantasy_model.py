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
df_18 = df_no_outliers[df_no_outliers['season_id'] == '2017-18']

# Next, let's normalize points in a new col. We're going to take the value, subtract the minumum value, and divide
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
    ['season_id']).apply(normalize_df)
print(df_normalized.sample(10))
