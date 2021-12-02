import pandas as pd
from IPython.core.display import display
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# a)
es_df = pd.read_csv('european-soccer.csv')
# display(es_df.head(10))

# b)
height_heading = es_df[['player_name', 'height', 'heading_accuracy']]
# display(height_heading.head())

height_values = height_heading['height']
# plt.hist(height_values)
# plt.show()

# c)
# print(es_df.shape)
df_nonull = es_df.dropna()
# print(df_nonull.shape)

# d)
# print(df_nonull.dtypes)
oscar_rating = es_df.loc[es_df['player_api_id'] == 3316, ['overall_rating']].values[0][0]
# print(oscar_rating)
df_rating = df_nonull[df_nonull['overall_rating'] >= oscar_rating]
# print(df_rating.shape)

# e)
df = df_rating[
    ['player_name', 'overall_rating', 'crossing',
     'finishing', 'heading_accuracy', 'short_passing',
     'dribbling', 'ball_control', 'acceleration',
     'sprint_speed', 'jumping', 'stamina',
     'strength', 'aggression', 'vision']
]
# print(df.shape)
# display(df.head(10))

# f)
df_f = pd.read_csv(
    'european-soccer-first100-knn.csv',
    sep=',',
    encoding='utf-8',
    decimal=".",
    index_col="player_name"
)

df_T = df_f.T
# display(df_T.head())


def distance(column1, column2): return np.linalg.norm(column1 - column2)


distances = df_T.apply(
    lambda column2: df_T.apply(
        lambda column1: distance(column1, column2)
    )
)

neighbours = distances['Oscar Sanchez'].drop('Oscar Sanchez').sort_values()
# display(neighbours.head()) # 5 most similar players
