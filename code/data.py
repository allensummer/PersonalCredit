# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 17:00:09 2017

@author: Administrator
"""

import pandas as pd

import numpy as np

class ReadClass():
    dataType = "train"
    dirPath = "K:\match\\"
    
    def __init__(self, dataType):
        self.dataType = dataType
    
    #读取银行数据
    def get_bank_detail(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","时间戳","交易类型","交易金额","工资收入标记"]
        return pd.read_csv(self.dirPath +self.dataType + "\\bank_detail_" + self.dataType + ".txt", names = IndexName, header = None)
    
    #信用卡账单记录
    def get_bill_detail(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","账单时间戳","银行id","上期账单金额","上期还款金额","信用卡额度","本期账单余额","本期账单最低还款额","消费笔数","本期账单金额","调整金额","循环利息","可用金额","预借现金额度","还款状态"]
        return pd.read_csv(self.dirPath +self.dataType + "\\bill_detail_" + self.dataType + ".txt", names = IndexName, header = None)
    
    #浏览器记录
    def get_browse_history(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","时间戳","浏览行为数据","浏览子行为编号"]
        return pd.read_csv(self.dirPath +self.dataType + "\\browse_history_" + self.dataType + ".txt", names = IndexName, header = None)

    #放款用户
    def get_loan_time(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","放款时间"]
        return pd.read_csv(self.dirPath +self.dataType + "\\loan_time_" + self.dataType + ".txt", names = IndexName, header = None)

    #逾期用户
    def get_overdue(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","样本标签"]
        return pd.read_csv(self.dirPath +self.dataType + "\\overdue_" + self.dataType + ".txt", names = IndexName, header = None)

    #逾期用户
    def get_user_info(self):
        #时间戳进行了函数变化，
        IndexName = ["用户id","性别","职业","教育程度","婚姻状态","户口类型"]
        return pd.read_csv(self.dirPath +self.dataType + "\\user_info_" + self.dataType + ".txt", names = IndexName, header = None)


class FeaturesClass():
    timeStages = []
    maxOperators = {}
    sumOperators = {}
    countOperator = {}
    def __init__(self):
        pass
    
    def addTime(self, time):
        if(len(time)==2):
            self.timeStage.append(time)
        else:
            print("time请设置为二维时间点")
    
    def addMaxOperator(self, column):
        self.maxOperators[column] = np.max

    def getMaxOperator(self):
        return self.maxOperators
    
    def addSumOperator(self, column):
        self.sumOperators[column] = np.sum
        
    def getSumOperator(self):
        return self.sumOperators
        
    def addCountOperator(self, column):
        self.countOperators[column] = np.count_nonzero

    def getCountOperator(self):
        return self.countOperator        


if __name__=="__main__":
    data = ReadClass("train")
    a = data.get_bank_detail();
    a.head()
    a = data.get_bill_detail();
    a.head()
    a = data.get_browse_history();
    a.head()
    a = data.get_loan_time();
    a.head()
    a = data.get_overdue();
    a.head()
    a = data.get_user_info();
    a.head();