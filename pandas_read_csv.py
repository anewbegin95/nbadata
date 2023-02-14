import pandas as pd
df = pd.read_csv(
    'nbadata/nba-stats-csv/player_general_traditional_per_game_data.csv'
    # ,usecols= ['player_id', 'season_id']
    ,index_col='player_id'
    )

df = pd.read_csv(
    'nbadata/nba-stats-csv/player_stats_total.csv'
)

df_slim = df.sample(20)

list_of_cols = ['player_name', 'ftm', 'fta']

print(df_slim[list_of_cols])
# print(list(df_slim))
# print(df_slim)
# print(df.corr())
# print(df.info())
# print(df.describe())
# print(df.columns)
# print(df.head(10))
# print(df.dtypes)