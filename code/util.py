# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:51:15 2017

@author: allen
"""

import pandas as pd

import numpy as np

def BinaryDataBalance(data, label, rate):
    positive = data[data[label]==1.0]
    negtive = data[data[label]== 0.0]

    pieces = [negtive.sample(int(len(positive)*rate)), positive]

    return pd.concat(pieces)

def get_importance_feature_name(X, Y):
    from sklearn.ensemble import ExtraTreesClassifier    
    #特征选择
    # Build a forest and compute the feature importances
    forest = ExtraTreesClassifier(n_estimators=200,
                                  random_state=0)                         
    
    forest.fit(X, Y)
    importances = forest.feature_importances_
    
    indices = np.argsort(importances)[::-1]
    
    importance_sort_feature = [X.columns[indices[f]] for f in range(X.shape[1])]
    
    return importance_sort_feature
def value_count(x, key_map, column_name):
    map_count={}    
    for i in key_map.keys():
        map_count[i] = 0
    value_count = x[column_name].value_counts()
    for i in value_count.index:
        map_count[i] += value_count[i]
    return pd.Series(map_count.values(), index=map_count.keys())