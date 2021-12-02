#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:47:44 2020

@author: sander
"""

import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import classification_report  
from matplotlib import pyplot as plt 

############### Task a ############### 

df = pd.read_csv('xAPI-Edu-Data.csv', sep=',', encoding='utf-8', decimal=".")
print(df.head())

raised_hands_avgs = df.groupby('Topic')['raisedhands'].mean()
print(type(raised_hands_avgs)) # This shows we're not dealing with a dataframe anymore, but a series
print(raised_hands_avgs.head()) # Notice here that we don't have two columns, we have the index and one column


x = raised_hands_avgs.index
y = raised_hands_avgs # Not really necessary, only for clarity. Remember, when dealing with a series, 
					  # the index is skipped when using the series (ie. even though it looks like it's
					  # two columns when looking the output from head(), it's in reality only a single column
					  # since the index isn't reqgarded as a column
					  
plt.xticks(rotation=90) # This rotates the topics so label don't overlap, but isn't strictly necessary

plt.bar(x, y)
plt.show()



############### Task b ############### 

# Looking at the names of the columns of the dataset, we can see that the column for parent satisfaction
# is named 'ParentschoolSatisfaction'. This column only has two values: Good and Bad. This is an indication
# that we should use a ClassificationTree, since we are dealing with discrete values (i.e, the outcome is
# two or more "categories"), opposed to continuous values (i.e. a simply a number), which would have been
# a regression tree
#
# Since the task states "[...] using *any* of the available attributes.", let's use the these columns:
# StageID, SectionID, raisedhands, VisITedResources, AnnouncementsView, Discussion, ParentAnsweringSurvey.

# Given that some of these columns aren't numerical, we have to convert them into a numberical equivalent.
# From the lesson on gitlab concerning desicion trees, we get:
df = pd.read_csv('xAPI-Edu-Data.csv', sep=',', encoding='utf-8', decimal=".")
print(df.head())

# First off, let's make a dataframe with only the columns we want
df1 = df[['ParentschoolSatisfaction', 'StageID', 'SectionID', 'raisedhands', 'VisITedResources', 'AnnouncementsView', 'Discussion', 'ParentAnsweringSurvey']] #NB! Note the double brackets here!
print(df1.head())

# Convert non-numeric columns
cleanup_nums = {"ParentschoolSatisfaction": {"Bad": 0, "Good": 1},
				"StageID": {"HighSchool": 2, "MiddleSchool": 1, "lowerlevel": 0},
                "SectionID": {"A": 0, "B": 1, "C": 2},
				"ParentAnsweringSurvey": {"No": 0, "Yes": 1}}

df1.replace(cleanup_nums, inplace=True)
print(df1.head())

# We want to predict parent satisfaction, so we remove that column into another variable
y = df1['ParentschoolSatisfaction']
# Afterwards we remove it from df1, and place the rest of the dataframe in a new one called X
X = df1.drop('ParentschoolSatisfaction', axis = 1)
print("Herp:\n" + str(X.head()))


# After this, one can basically follow the lesson from gitlab to a tee, the only
# exception is changing the class names on the second to last line

# We split the dataset horizontally. We use 20% for testing and 80% for training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Grow tree, using max_depth and/or min_impurity_decrease (gini) to manipulate depth
classifier = DecisionTreeClassifier(min_impurity_decrease=0.01, max_depth=5)  
classifier.fit(X_train, y_train)  

# Test tree
y_pred = classifier.predict(X_test) 
print(classification_report(y_test, y_pred))  

dotfile = open("./dtree1.dot", 'w')
ditfile = tree.export_graphviz(classifier, out_file = dotfile, feature_names = X.columns, class_names=['Bad', 'Good'])
dotfile.close()

# You could then take the produced dot-file (dtree1.dot) and paste its contents into https://webgraphviz.com to get
# a visual representation

