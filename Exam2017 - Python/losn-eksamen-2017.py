#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:35:56 2020

@author: sander
"""

import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn import tree
from matplotlib import pyplot as plt 

############### Task 3a ############### 

# The solution to this is very similar to the solution for the first task on the 2016 exam.
# The difference being we do not use grouby (we're not finding mean in this case), so we
# instead take a shortcut by using the value_counts() function. Note, value_counts() do 
# return a series, not a dataframe, so the same restrictions applies here as it did on the
# 2016 exam.

df = pd.read_csv('movie_metadata_simplified.csv', sep=',', encoding='utf-8', decimal=".")
#print(df.head())

# The name of the column which contains the year of the movie is 'title_year'. Knowing this, we can use the
# value_counts()-function from Pandas.
movies_per_year = df['title_year'].value_counts()
print(type(movies_per_year)) # This shows we're not dealing with a dataframe anymore, but a series
print(movies_per_year.head()) # Notice here that we don't have two columns, we have the index and one column


x = movies_per_year.index
y = movies_per_year   # Not really necessary, only for clarity. Remember, when dealing with a series, 
					  # the index is skipped when using the series (ie. even though it looks like it's
					  # two columns when looking the output from head(), it's in reality only a single column
					  # since the index isn't reqgarded as a column
					  
plt.xticks(rotation=90) # This rotates the topics so label don't overlap, but isn't strictly necessary

plt.bar(x, y)
plt.show()




############### Task 3b ############### 

df = pd.read_csv('movie_metadata.csv', sep=',', encoding='utf-8', decimal=".")
print(df['title_year'])


# The first one is really easy, as we just run the median() function on the column
median_all = df['imdb_score'].median()
print("All: " + str(median_all))


# The second part is a bit more involved, but still pretty easy. Here we use normal filtering in Pandas
# to create a new dataframe, before we use the same solution as we did above.

df_filtered = df[df['title_year'] == 1980] 
#print(df_filtered.head())

median_1980 = df_filtered['imdb_score'].median()
print("1980: " + str(median_1980))


############### Task 3c ############### 

# Given were supposed to find a number here, that is, a value that can be considered continuous, it
# seems reasonable to use a regression tree.
from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv('movie_metadata.csv', sep=',', encoding='utf-8', decimal=".")

# Lets first create a dataframe with only the columns we're interested in
df1 = df[['gross', 'imdb_score', 'num_voted_users']]
print(df1.head())

# If you try to run the code below this, you'll find that a ValueError occurs, due to some rows containing
# NaN, so we have to remove those rows.
df2 = df1.dropna(how='any')

# This is commented out, because it's something you wouldn't know that you'd have to
# do before you ran your code for the first time, and subsequently realized you had an absolutely humonguos tree.
# Make these two lines uncommented, and try to run the code again and look at the tree on webgraphviz.com 
#
# df2['gross'] = df2['gross'].div(1000000)
# df2['num_voted_users'] = df2['num_voted_users'].div(1000)
#
# Note: if you have trouble understanding the bit about .div(), don't worry about it.
# While it's something that can be done to "prune" trees, we haven't touched upon this
# way of doing things, and there won't be a task which would require this on bit on an exam.


# Again, following the lesson on gitlab
y = df2['gross'] 
X = df2.drop('gross', axis=1)  
print(X.head())


# We split the dataset horizontally. We use 20% for testing and 80% for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

# Grow tree, using max_depth and/or min_impurity_decrease (mse, Mean Squared Error)
regr = DecisionTreeRegressor(max_depth=6, min_impurity_decrease=5 ** 2, max_leaf_nodes=13)  
regr.fit(X_train, y_train)  

# Test tree
y_pred = regr.predict(X_test) 

print("Training score: " + format(regr.score(X_train,y_train)))
print("Testing score: " + format(regr.score(X_test,y_test)))

# "Display" tree
dotfile = open("./dtree2-2017.dot", 'w')
ditfile = tree.export_graphviz(regr, out_file = dotfile, feature_names = X.columns)
dotfile.close()


# This produces a *very* big tree. We can make the tree more presentable by doing as in the original
# solution, by dividing the gross by a million and the number of votes by a 1000. This could be done by
# using the div() function (line 87/88). After that, it'd be a matter of playing around with the value of
# min_impurity_decrease (line 105) to find a value which produces a tree that is somewhat sensible.



############### Task 3d ###############

# This task seems to be somewhat weirdly worded, with actor 1, 2, and 3. If you look at the CSV-file,
# there are three columns called actor_1_facebook_likes, actor_2_facebook_likes, actor_3_facebook_likes.
# Looking at the explanation in the appendix, we can see that this means they mean actors or actresses 
# which play the protagonist, the second main charater, and the third main character.
# However, the number of "facebook likes" in this context is somewhat obtuse, because we don't really
# know if the facebook likes are in context of that character for *a given movie*. Though, since they
# are separate columns and there seems to be a value for every(-ish) movie, one would almost just have
# to assume so.

# The solution to this would basically be exactly the same as the one for task 3c, but with different
# columns. Therefore, we just copy the code from 3b and change the column names.

df = pd.read_csv('movie_metadata.csv', sep=',', encoding='utf-8', decimal=".")

# Lets first create a dataframe with only the columns we're interested in
df1 = df[['gross', 'actor_1_facebook_likes', 'actor_2_facebook_likes', 'actor_3_facebook_likes']]

df2 = df1.dropna(how='any')

# In this case, we know already the we should adjust values to get a more readable tree
df2['gross'] = df2['gross'].div(1000000)
df2['actor_1_facebook_likes'] = df2['actor_1_facebook_likes'].div(1000)
df2['actor_2_facebook_likes'] = df2['actor_2_facebook_likes'].div(1000)
df2['actor_3_facebook_likes'] = df2['actor_3_facebook_likes'].div(1000)


# Again, following the lesson on gitlab
y = df2['gross'] 
X = df2.drop('gross', axis=1)  
print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

# Grow tree, using max_depth and/or min_impurity_decrease (mse, Mean Squared Error)
regr = DecisionTreeRegressor(max_depth=6, min_impurity_decrease=5 ** 2)  
regr.fit(X_train, y_train)  

# Test tree
y_pred = regr.predict(X_test) 

print("Training score: " + format(regr.score(X_train,y_train)))
print("Testing score: " + format(regr.score(X_test,y_test)))

# "Display" tree
dotfile = open("./dtree2-2017-3d.dot", 'w')
ditfile = tree.export_graphviz(regr, out_file = dotfile, feature_names = X.columns)
dotfile.close()

