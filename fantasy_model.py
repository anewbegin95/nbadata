"""
This model will be inspired by a few things, including k nearest neighbors (KNN) and factor-adjusted team similarites (FATS)
 from NBA math. We'll implement a manual model to find similar players.
Steps in this model:
    1. Normalize data acorss seasons
    2. Find the 10 most similar player seasons historically
    3. Rank and weight each of those 10 players season stats
    4. Look at 10 players following season's stats
    5. Use weighted averages to predict current players next season
    6. Rinse and repeat for every player in 2017 - 2018
Normalizing is crucial because averages change over time, and we want to know how similar players are to those averages. We want
 to look at statistic strength compared to the league as a whole. Changes can be minor year-to-year, but very different over long 
 spans of time.

To make things simple, we'll come up with one statistic called percent error to see how similar players are to each other. Meant
 to measure distance in statistics between numbers. Only distance will matter in this comparison. We may not want to weight stats
   the same (i.e.: blocks may not be weighted as highly as points)
"""

# Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Make a list of all of the columns that we use for scoring in daily / weekly matchup.
# There are two types of NBA fantasy leagues, but they take these statistics into consideration the same way.
stats = [
    'pts', 'min', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'ast', 'stl', 'tov', 'blk'
]

# Read in per season stats, which account for injury time outages better than per game stats, and scrub them.
csv = 'nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv'
df = pd.read_csv(
    csv, header=0
)

# Drop null value rows
df_cleaned = df.dropna(how='all')

# Remove outliers, specifically players who don't play much who are going to reduce our averages.
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

"""
We need to normalize our data. Scoring 22 ppg in 1993 isn't the same as scoring 22 ppg in 2023. The modern NBA features more attempts
 per game and higher rates of accuracy. Additionally, the introduction and wide-spread adoption of the three point shot has increased 
 scoring over time. In order to compare across seasons, we need to normalize data to compare performance fairly. We're going to 
 create a column that takes the a raw statistical value, subtracts the minumum value from that season, and divides by difference
 between max and min values from that season to normalize the stat.
"""


def normalize_col(col):
    normalized_input = (col - col.min()) / (col.max() - col.min())
    return normalized_input

# Create a new function which calls normalize_col and iterates through a dataframe


def normalize_df(df):
    for col in stats:
        df['{}_norm'.format(col)] = normalize_col(df[col])
    return df


# Create a grouped df grouped by season_id to run our function on 
df_normalized = grouped_df = df_no_outliers.groupby(
    ['season_id'], group_keys=True).apply(normalize_df)
"""
We need to calculate player distance, or percent error. This metric shows how close players' normalized stats are. Our goal is to
 find the ten players with the shortest distance across all stats. We'll create a function called called calc_distance that takes 
 two players as inputs and outputs their distance. To measure distance, we're going to use the euclidian distance between two 
 points. This measures the length of the distance between the two points. We can caluclate this with the square root function.
"""

def calc_distance(u, v):
    dist = np.sqrt(np.sum((u - v) ** 2))
    return dist


# Test two players and see how our function works
df_player_names = pd.read_csv(
    'nbadata/nba-stats-csv/player_info.csv')
# Join the df_normalized with a df with names to see names
df_normalized.reset_index(drop=True, inplace=True)
df_player_names.reset_index(drop=True, inplace=True)
df_normalized = pd.merge(df_normalized, df_player_names,
                         on=['player_id', 'season_id'], how='left').drop_duplicates()

# Move player_name toward the beginning of the dataframe
col_list = df_normalized.columns.tolist()
col_list = col_list[0:1] + col_list[-1:] + col_list[1:-1]
df_normalized = df_normalized[col_list]

# Another function we need to create is one that finds a row of data based on a player id and season id. To find this data,
# we need to iterate over the df until we find the row.


def find_player(input_df, player_id, player_season):
    for row in input_df.itertuples():
        if player_season == row.season_id and player_id == row.player_id:
            return row


# We need to be able to use our functions to find players with similar seasons. We're going to take stats from two players and put
# them in arrays. Then we'll use our calc distance to compare them and get a single value. This means we'll compare every single
# player's season against each player's season.
# We'll compare to Michael Kidd-Gilchrist in 2013-2014
current_player = 203077
current_season = '2013-14'
mkg_2013_14_vector = np.array([
    (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'pts_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'min_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fgm_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fga_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fg3m_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fg3a_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'ftm_norm']).item(
    ), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fta_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'oreb_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'dreb_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'ast_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'stl_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'tov_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'blk_norm']).item()
])
# print(mkg_2013_14_vector)

# We're going to use Jrue Holiday in 2016-17 as our test.
current_player = 201950
current_season = '2016-17'
current_player_vector = np.array([
    (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'pts_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'min_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fgm_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fga_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fg3m_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fg3a_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'ftm_norm']).item(
    ), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'fta_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'oreb_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'dreb_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'ast_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'stl_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'tov_norm']).item(), (df_normalized.loc[(df_normalized['player_id'] == current_player) & (df_normalized['season_id'] == current_season), 'blk_norm']).item()
])
# print(jrue_2016_17_vector)

# Now let's use the calc distance function for these two arrays. First we need to vectorize the function. This purpose is to
# transform this funciton into one that can return numpy arrays. Currently, the funciton takes floats as inputs, which can't
# be accepted in np lists
calc_distance_vector = np.vectorize(calc_distance)
distance_vector = calc_distance_vector(
    current_player_vector, mkg_2013_14_vector)
# print(distance_vector)

# Finally, we'll calculate the average percent error by dividing the sum total of the absolute difference by the number of cols.
avg_pct_error = np.sum(abs(distance_vector)) / len(distance_vector)
# print(avg_pct_error)

# Now that we have an approach for comparing two players, we can turn this into a for loop and compare multiple plaeyers.
# Let's create an empty list with the distance numbers and append them one at a time as we loop through.
player_distance = []

# Loop over rows in a dataframe with itertuples method.
for row in df_normalized.itertuples():
    compared_player_vector = np.array([
        row.pts_norm, row.min_norm, row.fgm_norm, row.fga_norm, row.fg3m_norm, row.fg3a_norm, row.ftm_norm, row.fta_norm, row.oreb_norm, row.dreb_norm, row.ast_norm, row.stl_norm, row.tov_norm, row.blk_norm
    ])

    calc_distance_vector = np.vectorize(calc_distance)
    distance_vector = calc_distance_vector(
        current_player_vector, compared_player_vector)
    avg_pct_error = np.sum(abs(distance_vector)) / len(distance_vector)
    player_distance.append(avg_pct_error)
    player = row.player_name
    # print('Done with ' + str(player) + '. Percent error was ' + str((round((1 - avg_pct_error), 3) * 100)) + '%.')

df_normalized['ranking'] = player_distance
df_ranked = df_normalized.sort_values('ranking', ascending=True)
df_ranked.reset_index(drop=True, inplace=True)
# print(df_ranked)

# Now that we can compare seasons and sort on player error, we can find the ten players with the
# most similar seasons to a single player. Now we need to look at the next season for those ten
# players, average that following season together, and use that to project our selected player's
# next season.

# The average we're taking will be a weighted average. If one of the 10 players had a small distance,
# indicating similar player behavior, we'll weight that number heavier. We'll add logic to also
# weight for the same player.

# First, we need a list of every season id
seasons_list = df_normalized['season_id'].unique().tolist()
# print(seasons_list)

# For loop to go over each stat, multipy value by weight, and get weighted avg
projected_stats_dict = {}

for col in stats:
    sum_stat = 0
    sum_weight = 0
    for index, row in df_ranked[1:11].iterrows():
        if row.season_id == '2017-18':
            continue
        if row.season_id == '2018-19':
            continue
        weight = (1 / row.ranking)
        next_season_id = seasons_list[(seasons_list.index(row.season_id) + 1)]
        if next_season_id == None:
            continue
        player_next_season = find_player(df_ranked, row.player_id, next_season_id)
        if player_next_season == None:
            continue
        sum_stat += getattr(player_next_season, col) * weight
        sum_weight += weight
    projected_stats_dict['proj_season_id'] = seasons_list[(seasons_list.index(current_season) + 1)]
    projected_stats_dict['proj_' + col] = (sum_stat / sum_weight)
print(projected_stats_dict)

"""
Create player comparison function that takes a dataframe, a current player id, and a season,
and outputs projected stats for player's next season. Then, loop over every player in draft to get
their projected stats for next season. Compare to actuals to see accuracy.
"""

def player_comparison(df, current_player_season, current_player_id):
    # If player doesn't exist in dataframe, print that player can't be found
    if ((df['season_id'] == current_player_season)  & (df['player_id'] == current_player_id)).any(False):
        print('Can\'t find player with id {} and season {}'.format(current_player_id, current_player_season))
        return
    
    for row in df.itertuples():
        if current_player_season == row['season_id'] and current_player_id == row['player_id']:
            current_player_id = row.player_id
            break

    current_player_vector = np.array([df
        (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'pts_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'min_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'fgm_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'fga_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'fg3m_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'fg3a_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'ftm_norm']).item(
        ), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'fta_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df_normalized['season_id'] == current_player_season), 'oreb_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'dreb_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'ast_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'stl_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'tov_norm']).item(), (df.loc[(df['player_id'] == current_player_id) & (df['season_id'] == current_player_season), 'blk_norm']).item()
    ])
    print('Projecting player_id {0} for season {1}'.format(current_player_id, seasons_list[(seasons_list.index(row.season_id) + 1)]))
    
    player_distance = []

    for row in df.itertuples():
        compared_player_vector = np.array([
            row.pts_norm, row.min_norm, row.fgm_norm, row.fga_norm, row.fg3m_norm, row.fg3a_norm, row.ftm_norm, row.fta_norm, row.oreb_norm, row.dreb_norm, row.ast_norm, row.stl_norm, row.tov_norm, row.blk_norm
        ])
        
        calc_distance_vector = np.vectorize(calc_distance)
        distance_vector = calc_distance_vector(
            current_player_vector, compared_player_vector)
        avg_pct_error = np.sum(abs(distance_vector)) / len(distance_vector)
        player_distance.append(avg_pct_error)
    
    df['ranking'] = player_distance

    df_ranked = df.sort_values('distance')

    df_ranked.reset_index(drop=True, inplace=True)

    stats = [
        'pts', 'min', 'fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'ast', 'stl', 'tov', 'blk'
    ]

    projected_stats_dict = {}

    for col in stats:
        sum_stat = 0
        sum_weight = 0
        for index, row in df_ranked[1:11].iterrows():
            if row.season_id == '2018-19':
                continue
            weight = (1 / row.ranking)
            next_season_id = seasons_list[(seasons_list.index(row.season_id) + 1)]
            player_next_season = find_player(df_ranked, row.player_id, next_season_id)
            if player_next_season == None:
                continue
            sum_stat += getattr(player_next_season, col) * weight
            sum_weight += weight
        projected_stats_dict['proj_season_id'] = seasons_list[(seasons_list.index(current_season) + 1)]
        projected_stats_dict['proj_' + col] = (sum_stat / sum_weight)

    return projected_stats