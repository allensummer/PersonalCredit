# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:49:44 2017

@author: allen
"""


import pandas as pd

import numpy as np

import featureExtractor 

import data

import util

from sklearn import svm
from sklearn.model_selection import cross_val_score
from scipy.stats import ks_2samp
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestClassifier


class person_credit_model():
    def __init__(self):
        pass
    def get_feature_extractor(self):
        feature = featureExtractor.FeatureExtractor()
        
        feature.add_time("1", [0, 30000000])
        feature.add_time("2", [30000000, 35000000])
        feature.add_time("3", [35000000, 40000000])
        feature.add_time("4", [45000000, 60000000])
        feature.add_time("5", [0, 6000000000])
        
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.max, "max")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.sum, "sum")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.average, "average")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.std, "std")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.min, "min")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.mean, "mean")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.median, "median")
        feature.add_simple_operator("bank", "jiaoyi_jin_e", np.count_nonzero, "count_nonzero")
        
        feature.add_simple_operator("bank", "jiaoyi_leixing", np.max, "max")
        feature.add_simple_operator("bank", "jiaoyi_leixing", np.sum, "sum")
        feature.add_simple_operator("bank", "jiaoyi_leixing", np.std, "std")
        feature.add_simple_operator("bank", "jiaoyi_leixing", np.mean, "mean")
        feature.add_simple_operator("bank", "jiaoyi_leixing", np.min, "min")
        
        feature.add_simple_operator("bank", "gongzi_shouru_biaoji", np.count_nonzero, "sum")

        feature.add_simple_operator("bill", "last_bill_amount", np.max, "max")
        feature.add_simple_operator("bill", "last_bill_amount", np.min, "min")
        
        feature.add_simple_operator("bill", "last_huangkuan_jin_e", np.max, "max")
        feature.add_simple_operator("bill", "last_huangkuan_jin_e", np.min, "min")
        
        feature.add_simple_operator("bill", "credit_e_du", np.max, "max")
        feature.add_simple_operator("bill", "credit_e_du", np.min, "min")
        
        feature.add_simple_operator("bill", "benqi_zhangdan_e_du", np.max, "max")
        feature.add_simple_operator("bill", "benqi_zhangdan_e_du", np.min, "min")
        
        feature.add_simple_operator("bill", "benqi_zhangdan_zuidi_e_du", np.max, "max")
        feature.add_simple_operator("bill", "benqi_zhangdan_zuidi_e_du", np.min, "min")
        
        feature.add_simple_operator("bill", "consume_bishu", np.max, "max")
        feature.add_simple_operator("bill", "consume_bishu", np.min, "min")
        
        feature.add_simple_operator("bill", "benqi_zhangdan_jin_e", np.max, "max")
        feature.add_simple_operator("bill", "benqi_zhangdan_jin_e", np.min, "min")
        
        feature.add_simple_operator("bill", "tiaozheng_jin_e", np.max, "max")
        feature.add_simple_operator("bill", "tiaozheng_jin_e", np.min, "min")
        
        feature.add_simple_operator("bill", "xunhuang_lixi", np.max, "max")
        feature.add_simple_operator("bill", "xunhuang_lixi", np.min, "min")
        
        feature.add_simple_operator("bill", "keyong_jin_e", np.max, "max")
        feature.add_simple_operator("bill", "keyong_jin_e", np.min, "min")
        
        feature.add_simple_operator("bill", "yujie_xianjing_e_du", np.max, "max")
        feature.add_simple_operator("bill", "yujie_xianjing_e_du", np.min, "min")
        
        feature.add_simple_operator("bill", "huangkuan_zhuangtai", np.max, "max")
        feature.add_simple_operator("bill", "huangkuan_zhuangtai", np.min, "min")
        
        feature.add_simple_operator("browse", "browse_action", np.count_nonzero, "count_nonzero")


        feature.add_simple_operator("loan", "time", np.count_nonzero, "count_nonzero")
        
        feature.add_overall_operator("bill", "time", np.min, "min")
        feature.add_overall_operator("browse", "time", np.min, "min")
        feature.add_overall_operator("bank", "time", np.min, "min")
        
        feature.add_overall_operator("bill", "time", np.max, "max")
        feature.add_overall_operator("browse", "time", np.max, "max")
        feature.add_overall_operator("bank", "time", np.max, "max")        
        
        feature.add_overall_operator("bill", "time", np.mean, "mean")
        feature.add_overall_operator("browse", "time", np.mean, "mean")
        feature.add_overall_operator("bank", "time", np.mean, "mean")        
#        
        return feature
    def get_feature_data(self):
        feature =  self.get_feature_extractor() 
        
        readData = data.ReadClass()
        overdue = readData.get_overdue();
        trainData = readData.get_train_data();
        feature.set_data(trainData, 5952662481, ['bank', 'bill', 'browse', 'loan'])
        
        #读取训练数据集
        overdue = trainData['overdue']
        user_info = trainData['user_info']
        train = pd.merge(overdue, user_info, how = "left", on='id').fillna(0);

        train = pd.merge(train, trainData["loan"], how = "left", on='id').fillna(0);
                
        
        simple_features = feature.get_simple_feature()
        
        train = pd.merge(train, simple_features, how = "left", left_on='id', right_index=True).fillna(0);
        
        #读取数据集
        predData = readData.get_test_data();
        feature.set_data(predData, 5952662500, ['bank', 'bill', 'browse', 'loan'])
        
        test_simple_features = feature.get_simple_feature()
        
        user_id = predData['user_id']
        user_info = predData['user_info']
        pred = pd.merge(user_id, user_info, how = "left", on='id').fillna(0);
        pred = pd.merge(pred, trainData["loan"], how = "left", on='id').fillna(0);
        pred = pd.merge(pred, test_simple_features, how = "left", left_on='id', right_index=True).fillna(0);
        
        return train, pred
    
    def evaluate_KS(self, clf, X, Y):
        train_pred = clf.predict_proba(X)[:, 1]

        print ks_2samp(train_pred, Y)
    
    def get_pred_result(self, X, Y, pred, importance_features):
            #建立svm模型
        clf = svm.SVC(probability = True, class_weight ={0:1, 1:1.55})
        
        #标准化
        standarModel = StandardScaler().fit(X)
        
        X = standarModel.transform(X)
        
        #拟合
        clf = clf.fit(X, Y)
        
        pred_standard_X = standarModel.transform(pred.loc[:, importance_features])
        
        pred["prediction"] = clf.predict_proba(pred_standard_X)[:, 1]
        
        pred.loc[:, ["id", "prediction"]].to_csv("pred.csv", index = False, header = ['userid','probability'])
        


pm = person_credit_model()

train, pred = pm.get_feature_data()


#数据平衡
balance_train = util.BinaryDataBalance(train, "exceed_label", 1)

X = balance_train.loc[:, balance_train.columns[2:]]
Y = balance_train['exceed_label']

#特征选择
#all_importance_features = util.get_importance_feature_name(X, Y)
#
#importance_features = all_importance_features[:]
#
#print len(importance_features)
#
#X = X.loc[:,importance_features]

print len(X.columns)
#划分训练测试集
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

clf = RandomForestClassifier(n_estimators=200, max_depth=None,
 min_samples_split=2, random_state=0)

#from sklearn.decomposition import TruncatedSVD
#
#svd = TruncatedSVD(n_components=8, n_iter=7, random_state=42)
#svd = svd.fit(balance_train) 
#
#svd_X = svd.transform(balance_train)
#print 1 - sum(Y)/(1.0 * len(Y))

scores = cross_val_score(clf, X, Y)

print scores

#print scores
#
#def disperse_count(df, column_name):
#    return df[column_name].value_counts()

#
#
#print "开始模型训练"
#clf = svm.SVC()
#
#standarModel = StandardScaler().fit(train.loc[:,importance_features])
#
#X = standarModel.transform(X)
#
#clf = clf.fit(X, Y)
#
#print "训练完成"
#
#pred_y = clf.predict(train.loc[:,importance_features])
#
#print sum(pred_y == train['exceed_label'])/(48413.0 + 7183.0)


#scores = cross_val_score(clf, train.loc[:,importance_features], train['exceed_label'])
#
#print scores.mean()  

