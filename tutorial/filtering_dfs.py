## It's easy to filter df's on columns and series.
import pandas as pd
import numpy as np

## Import our player stats data.
df = pd.read_csv('nbadata/nba-stats-csv/nba_season_stats.csv')

## First, let's see a sample of the data
# print(df.columns)

## Let's say we only want to see players who play for the Celtics.
## First, pandas evaluates whether team is the Celtics and says if the condition is T or F.
## To get the results, we need to pass this into a new set of square brackets.
is_playing_for_bos = (df['Tm'] == 'BOS')
bos_df = df[is_playing_for_bos]
# print(bos_df)

## For more advanced filtering, we can use mathematical and logical operators to filter data.
## Let's do this to find all the players on Toronto OR Boston.
is_playing_for_tor = (df['Tm'] == 'TOR')

bos_or_tor_df = df[is_playing_for_bos | is_playing_for_tor]
bos_or_tor_df.sort_values(by='Tm',inplace=True)

print(bos_or_tor_df)

## We can use the AND operator to see multiple conditions that must be true.
## Let's find all the players for the C's who started more than 10 games
is_starting_more_than_ten_games = (df['GS'] > 10)

bos_gs_more_than_ten = df[is_playing_for_bos & is_starting_more_than_ten_games]
bos_gs_more_than_ten.sort_values(by='GS', inplace=True)

print(bos_gs_more_than_ten)

## Let's go for lots of conditions! First, we'll create boolean variables to see if
## anyone had 50% FG shooting, 40% 3PT shooting, and 90% FT shooting
is_50_fg_pct = (df['FG%'] > .5)
is_40_3pt_pct = (df['3P%'] > .4)
is_90_ft_pct = (df['FT%'] > .9)

is_50_40_90_club = (is_50_fg_pct & is_40_3pt_pct & is_90_ft_pct)

## Let's see who was in the 50% / 40% / 90% club for Boston (no one was).
bos_50_40_90_club = df[is_playing_for_bos & is_50_40_90_club]
print(bos_50_40_90_club)

## Let's see if anyone in the league was.
## Two dudes with 0 GS were in the club, but no one else.
is_50_40_90_club_df = df[is_50_40_90_club]
print(is_50_40_90_club_df)

## Another way to filter dataframes is wht the .isin() method.
## We pass pandas a list and pandas will iterate through the list to see all of the
## values present.

## Create a list of teams.
team_list = ['OKC', 'LAL', 'CHI']

## Use the .isin() method to filter for just the teams in the list.
team_list_df = df[df['Tm'].isin(team_list)]
team_list_df.sort_values(by='Tm', inplace=True)
print(team_list_df)