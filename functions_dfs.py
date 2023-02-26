## Somtimes, we might want to do a funciton on every row in df or every row in a specific col / series.
## We can do this with the apply funciton. It can be done to clean up functions or normalize values.

## The first parameter the apply method expects is some type of custom function. It passes every series val
## to function and returns a new series object, which we can eitehr pass into the same col or a new col.

import pandas as pd

url = 'nbadata/nba-stats-csv/player_stats_total.csv'
df = pd.read_csv(url)

df_sample = df.sample(5)
# print(df_sample)

## One of the cols in here is age. Let's add a year to each player's age by creating a custom age function
## that does so and then replaces the existing age column.
def add_year (current_age):
    new_age = current_age + 1
    return new_age

## Running this will return vals as a series
# print(df['age'].apply(add_year))

## We can also use apply on multiple columns within a row. Let's divide total points scored by total games 
## played to get points per game.

## Pandas passes row values to the apply method if we call them in a unique way. It'll pass these in a list 
## which means it'll use index positioning from the dataframe.

## Let's first get the points for a few players.
player_stats = {
    'player_name' : ['Lebron', 'Dirk', 'Wade', 'Curry', 'George']
    ,'season_id' : ['2017-18', '2017-18', '2017-18', '2017-18', '2017-18']
    ,'total_points' : [1251, 927, 765, 1346, 1734]
    ,'games_played' : [82, 77, 81, 51, 79]
}
df = pd.DataFrame(player_stats)

def ppg(row):
    gp = row[3]
    pts = row[2]
    ppg = pts / gp
    return ppg

df['ppg'] = round(df.apply(ppg, axis = 1),2)
# print(df)

## Let's look at another example using columns instead of positions.
## We'll create a free throw percentage calculator.
url = 'nbadata/nba-stats-csv/player_stats_total.csv'
df = pd.read_csv(url)

def ft_pct(row):
    ft_pct = round((row['ftm'] / (row['fta'] + .00001)),2)
    return ft_pct

df['ft_pct'] = df.apply(ft_pct ,axis=1)
# print(df.sample(5))

## This above calc made a calculation of ft per season, but what if we wanted to make one for the player's whole career?
## We'd need to sumarize by player and first get the total of fta and ftm.
player = df.groupby(['player_id', 'player_name'])
# print(player)
player_career_fts = player['ftm', 'fta'].sum()
player_career_fts['ft_pct'] = player_career_fts.apply(ft_pct, axis = 1)
player_career_fts.sort_values('fta', inplace = True ,ascending = False)
player_career_fts.reset_index(inplace = True)
print(player_career_fts)