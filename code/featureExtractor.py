# -*- coding: utf-8 -*-
"""
Created on Sun Jan 08 09:45:09 2017

@author: allen
"""
import pandas as pd

class FeatureExtractor():
    feature = None
    timeStages = {}#时间段
    over_all_time = {}   #全局时间 
    
    simpleFeature = {}  #时间段操作
    operator_alias = {} #时间段操作命名

    over_all_time_feature = {}  #全局操作
    over_all_time_feature_alias = {}    #全局操作命名

    type_count_feature = {}    #类型统计特征
    type_count_feature_alias = {}   #类型特征统计命名
    
    data = None;    #相对时间点
    time_table = None;  

    def add_time(self, time_name, time):
        if(len(time)==2):
            self.timeStages[time_name] = time
        else:
            print("time请设置为二维时间点")
    
    #增加全局特征
    def add_overall_operator(self, table, column,  operate, alias):
        if table in self.over_all_time_feature.keys():
            if column in self.over_all_time_feature[table].keys():
                self.over_all_time_feature[table][column].append(operate)
                self.over_all_time_feature_alias[table][column].append(alias)
            else:
                self.over_all_time_feature[table][column] = [operate]
                self.over_all_time_feature_alias[table][column] = [alias]
        else:
            self.over_all_time_feature[table] = {column:[operate]}
            self.over_all_time_feature_alias[table] = {column:[alias]}
           
    #增加简单时间特征
    def add_simple_operator(self, table, column,  operate, alias):
        if table in self.simpleFeature.keys():
            if column in self.simpleFeature[table].keys():
                self.simpleFeature[table][column].append(operate)
                self.operator_alias[table][column].append(alias)
            else:
                self.simpleFeature[table][column] = [operate]
                self.operator_alias[table][column] = [alias]
        else:
            self.simpleFeature[table] = {column:[operate]}
            self.operator_alias[table] = {column:[alias]}
            
    #增加种类计数特征
    def add_type_count_operator(self, table, column, alias):
        if table in self.type_count_feature.keys():
            if column in self.type_count_feature[table].keys():
                self.type_count_feature[table].append(column)
                self.type_count_feature_alias[table].append(alias)
            else:
                self.type_count_feature[table] = [column]
                self.operator_alias[table] = [alias]
        else:
            self.type_count_feature[table] = [column]
            self.operator_alias[table] = [alias]
    
    #导入数据，将时间转换成相对时间
    def set_data(self, data, maxTime, time_table):
        self.data = data
        for i in time_table:
            self.data[i]['time'] = maxTime - data[i]['time'] 
    
    #得到简单的特征
    def get_simple_feature(self):
        agg_data = []
        #事件相关的特征
        for i in self.timeStages.keys():
            print i
            for tableName in self.simpleFeature.keys():
                data_buf = self.data[tableName]

                data_buf = data_buf[data_buf['time'] >= self.timeStages[i][0]]

                data_buf = data_buf[data_buf['time'] < self.timeStages[i][1]]

                data_buf = data_buf.groupby('id').agg(self.simpleFeature[tableName])

                #命名
                data_column = []
                
                for column in self.operator_alias[tableName].keys():
                    data_column += [i + "_" + tableName + "_" + column+ "_" + alias for alias in self.operator_alias[tableName][column]]
                data_buf.columns= data_column
               
                
                agg_data.append(data_buf)
        print "len ", len(agg_data)
        #全局相关的特征
        for tableName in self.over_all_time_feature.keys():
            print tableName
            data_buf = self.data[tableName]

            data_buf = data_buf.groupby('id').agg(self.over_all_time_feature[tableName])

            #命名
            data_column = []
            
            for column in self.over_all_time_feature_alias[tableName].keys():
                data_column += ["overall_" + tableName + "_" + column+ "_" + alias for alias in self.over_all_time_feature_alias[tableName][column]]
            data_buf.columns= data_column
            
            agg_data.append(data_buf)
        print "overall len ", len(agg_data)
        
        agg_data = pd.concat(agg_data, axis=1)
        return agg_data
    
    def get_type_count_feature(self):
        agg_data = []
        #事件相关的特征
        for i in self.timeStages.keys():
            print i
            for tableName in self.simpleFeature.keys():
                data_buf = self.data[tableName]

                data_buf = data_buf[data_buf['time'] >= self.timeStages[i][0]]

                data_buf = data_buf[data_buf['time'] < self.timeStages[i][1]]

                data_buf = data_buf.groupby('id').agg(self.simpleFeature[tableName])

                #命名
                data_column = []
                
                for column in self.operator_alias[tableName].keys():
                    data_column += [i + "_" + tableName + "_" + column+ "_" + alias for alias in self.operator_alias[tableName][column]]
                data_buf.columns= data_column
               
                
                agg_data.append(data_buf)
        print "len ", len(agg_data)
    
    def value_count(self, x, key_map, column_name):
        map_count=key_map.copy()
        value_count = x[column_name].value_counts()
        for i in value_count.keys():
            map_count[column_name + "_" + str(i)] += value_count[i]
        return pd.Series(map_count.values(), index=map_count.keys())
        
    def type_count(self, data, group_name, column_name):
        key_map = data[column_name].value_counts()
        key_map_alias = {}
        for i in key_map.index:
            key_map_alias[column_name + "_" + str(i)] = 0
        return data.groupby(group_name).apply(lambda x: self.value_count(x, key_map_alias, column_name))

