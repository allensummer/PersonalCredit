# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 17:00:09 2017

@author: Administrator
"""

import pandas as pd

import numpy as np


class ReadClass():
    dataType = "train"
    dirPath = "..\\"
    
    def __init__(self, dataType):
        self.dataType = dataType
    
    #读取银行数据
    def get_bank_detail(self):
        #用户id,时间戳,交易类型,交易金额,工资收入标记
        IndexName = ["id","time","jiaoyi_leixing","jiaoyi_jin_e","gongzi_shouru_biaoji"]
        return pd.read_csv(self.dirPath +self.dataType + "\\bank_detail_" + self.dataType + ".txt", names = IndexName, header = None)
    
    #信用卡账单记录
    def get_bill_detail(self):
        #用户id,账单时间戳,银行id,上期账单金额,上期还款金额,信用卡额度,本期账单余额,本期账单最低还款额,消费笔数,本期账单金额,调整金额,循环利息,可用金额,预借现金额度,还款状态
        IndexName = ["id","time","bank_id","last_bill_amount","last_huangkuan_jin_e","credit_e_du","benqi_zhangdan_e_du","benqi_zhangdan_zuidi_e_du","consume_jin_e","benqi_zhangdan_jin_e","tiaozheng_jin_e","xunhuang_lixi","keyong_jin_e","yujie_xianjing_e_du","huangkuan_zhuangtai"]
        return pd.read_csv(self.dirPath +self.dataType + "\\bill_detail_" + self.dataType + ".txt", names = IndexName, header = None)
    
    #浏览器记录
    def get_browse_history(self):
        #  用户id,时间戳,浏览行为数据,浏览子行为编号	
        IndexName = ["id","time","browse_action","browse_subaction_id"]
        return pd.read_csv(self.dirPath +self.dataType + "\\browse_history_" + self.dataType + ".txt", names = IndexName, header = None)

    #放款用户
    def get_loan_time(self):
        #用户id,放款时间，
        IndexName = ["id","time"]
        return pd.read_csv(self.dirPath +self.dataType + "\\loan_time_" + self.dataType + ".txt", names = IndexName, header = None)

    #逾期用户
    def get_overdue(self):
        #用户id,样本标签
        IndexName = ["id","exceed_label"]
        return pd.read_csv(self.dirPath +self.dataType + "\\overdue_" + self.dataType + ".txt", names = IndexName, header = None)

    #逾期用户
    def get_user_info(self):
        # 用户id,性别,职业,教育程度,婚姻状态,户口类型
        IndexName = ["id","gender","profession","education","marry","acount_type"]
        return pd.read_csv(self.dirPath + self.dataType + "\\user_info_" + self.dataType + ".txt", names = IndexName, header = None)

    def get_usersID(self):
        IndexName = ["id"]
        return pd.read_csv(self.dirPath + self.dataType + "\\usersID_" + self.dataType + ".txt", names = IndexName, header = None)
    
    def get_train_data(self):
        self.dataType = "train"
        data = {}
        data['bank'] = self.get_bank_detail()
        data['bill'] = self.get_bill_detail()
        data['browse'] = self.get_browse_history()
        data['loan'] = self.get_loan_time()
        data['user_info'] = self.get_user_info()
        #训练集与测试集不一样的地方        
        data['overdue'] = self.get_overdue()
        
    def get_test_data(self):
        self.dataType = "test"
        data = {}
        data['bank'] = self.get_bank_detail()
        data['bill'] = self.get_bill_detail()
        data['browse'] = self.get_browse_history()
        data['loan'] = self.get_loan_time()
        data['user_info'] = self.get_user_info()
        #训练集与测试集不一样的地方        
        data['user_id'] = self.get_usersID()
        
        
class FeaturesConfigurationClass():
    timeStages = {}
    maxOperators = {}
    sumOperators = {}
    countOperator = {}
    maxTime = 0
    def __init__(self, maxTime):
        self.maxTime = maxTime
    
    def addTime(self, time_name, time):
        if(len(time)==2):
            self.timeStage[time_name] = time
        else:
            print("time请设置为二维时间点")
    
    def addMaxOperator(self, column, table):
        if table in self.maxOperators.keys():
            self.maxOperators[table].append(column)
        else:
            self.maxOperators[table] = [column]
    def addSumOperator(self, column, table):
        if table in self.sumOperators.keys():
            self.sumOperators[table].append(column)
        else:
            self.sumOperators[table] = [column]
        
    def addCountOperator(self, column, table):
        if table in self.countOperators.keys():
            self.countOperators[table].append(column)
        else:
            self.countOperators[table] = [column]


class FeatureExtractor():
    feature = None
    def __init__(self, feature):
        self.feature = feature
    
    def get_max_feature(self):
        agg = []
        
        
    
def BinaryDataBalance(data, label, rate):
    positive = data[data[label]==1.0]
    negtive = data[data[label]== 0.0]

    pieces = [negtive.sample(int(len(positive)*rate)), positive]

    return pd.concat(pieces)
    
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import cross_val_score
#from sklearn import svm



# 0.0版本
#    data = ReadClass("train")
#    overdue = data.get_overdue();
#    user_info = data.get_user_info();
#    train = pd.merge(user_info, overdue,left_on='id', right_index=True,
#                      how='left', sort=False).fillna(0);
#    train = BinaryDataBalance(train, "exceed_label", 1.1)
#    print len(train)
#    #分类模型
#    #随机森林
#    clf = clf = RandomForestClassifier(n_estimators=10, max_depth=3,
#     min_samples_split=2, random_state=0)
#    #svm
##    clf = svm.SVC(probability = True)    
#    
#    
#    scores = cross_val_score(clf, train.loc[:, ["gender","profession","education","marry","acount_type"]], train['exceed_label'])
#
#    print scores.mean()  
#    clf = clf.fit(train.loc[:, ["gender","profession","education","marry","acount_type"]], train['exceed_label'])    
#    
#    
#    test_data = ReadClass("test")
#    #test_user = test_data.get_usersID()
#    test_user_info = test_data.get_user_info()
#    #test = pd.merge(test_user, test_user_info,left_on='id', right_index=True,
#     #                 how='left', sort=False).fillna(0);
#    test_user_info['prediction'] = clf.predict(test_user_info.loc[:, ["gender","profession","education","marry","acount_type"]])
#    print len(test_user_info)
#    print np.sum(test_user_info['prediction'])
#    
#    test_user_info.loc[:, ["id", "prediction"]].to_csv("pred.csv", index = False, header = False)
#    
if __name__=="__main__":
    data = ReadClass("train")
    overdue = data.get_overdue();
    user_info = data.get_bank_detail();
def get_letter_type(letter):
 if letter.lower() in 'aeiou':
     return 'vowel'
 else:
     return 'consonant'