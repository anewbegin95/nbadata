import pandas as pd

lakers_dict = {
    'first_name' : ['Lebron', 'Kyle', 'Lonzo', 'Brandon', 'Josh'],
    'last_name' : ['James', 'Kuzma', 'Ball', 'Ingram', 'Hart'],
    'ppg' : [27.4, 18.7, 9.9, 18.3, 7.8],
    'apg' : [8.3, 2.5, 5.4, 3.0, 1.4],
    'rpg' : [8.5, 5.5, 5.3, 5.1, 3.7]
}

lakers_stats = pd.DataFrame(lakers_dict, index = ['PF1','PF2','PG','SF','SG'])
print(lakers_stats)

last_night = [['Lebron', 4, 6], ['Kuzma', 2, 3], ['Ball', 4, 4]]
last_night_stats = pd.DataFrame(last_night, columns = ['player', 'oreb', 'dreb'])
print(last_night_stats)