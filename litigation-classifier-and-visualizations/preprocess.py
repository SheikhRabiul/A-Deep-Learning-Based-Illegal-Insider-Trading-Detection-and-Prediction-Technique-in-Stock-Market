# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:03:37 2018
Modified on Thu July 18
@created by: Sheikh Rabiul Islam ; sislam42@students.tntech.edu
Purpose: preprocess the data so that it can be feeded in to Machine Learning Alogorithms.
Input: infected logs file in data/infected/ folder in json format
       non infected logs file in data/non_infected/ folder in json floder
Output: feature vector in result/ folder
        feature vector index mapping in result folder
        Interim result are stored in result/interim/ folder. i.e., filtered logs
"""
# configure folder path here
folder_path_infected = "data/infected/"
folder_path_non_infected = "data/non_infected/"
folder_path_result = "result/"
folder_path_result_interim = "result/interim/"
from textblob import TextBlob as tb

#import modules
import os
import pandas as pd
import numpy as np
from generalFunctions import *

#global containers
features = []
features_infected = []
features_non_infected = []

#list of words that we do not want to consider as feature
stopwords = set(w.rstrip() for w in open('stopwords.txt'))
wildcards = set(w.rstrip() for w in open('wildcards.txt'))

# loop through individual logs, filter it more, build feature database, add new if not seen before. 
def build_features(path, file_name):
    list_row = []   
    file_path = os.path.join(path, file_name)
    #print(file_path)
    data_df = pd.read_csv(file_path)
    #print(data_df)
    for i, r in data_df.iterrows():
        #print("i",i)
        #print(r)
        
        title = r['title']
        litigation = r['lt']      
        #print(litigation)
        litigation_combined = str(title) + str(litigation)
        tbb  = tb(litigation_combined)
        litigation_combined = tbb.words
        #print(litigation_combined)
        
        row =[]
        for i in range(0,len(litigation_combined)):
            if len(litigation_combined[i]) > 2 and  len(litigation_combined[i]) < 11 and litigation_combined[i].lower() not in stopwords:
                val = str(litigation_combined[i])
                #val ="%r"%val #converting into raw string
                if val.isdigit():
                    val = str(len(val)) + "digit"
                row.append(val)
                #print("row")
        list_row.append(row)   
    #return a list of list. each element of the list contain
    # log features for an individual logs and the inner list contain the individual features of that logs.
    #print(list_row)
    return list_row




print("*******************************************************************")
print ("Populating features from the infected logs (showing first 5) ... ")
print("*******************************************************************")
for filename in os.listdir(folder_path_infected):
    if filename.endswith('.csv'):
        print ("starting file %s ... " % filename)
        path = folder_path_infected
        try:
            #features_infected = build_features(filename, wls)
            features_infected = features_infected + build_features(path,filename)
            #print(features_infected)
            print("\n")
        except:
            pass
        

print("*******************************************************************")
print ("Populating features from the non infected logs (showing first 5) ... ")
print("*******************************************************************")
for filename in os.listdir(folder_path_non_infected):
    if filename.endswith('.csv'):
        print ("starting file %s ... " % filename)
        path = folder_path_non_infected
        try:
            #features_non_infected = build_features(filename, wls)
            features_non_infected = features_non_infected + build_features(path,filename)
            print("\n")
        except:
            pass


print("*******************************************************************")
print("first 5 infected features:")
print("*******************************************************************")
print(features_infected[:5])

print("*******************************************************************")
print("first 5 non-infected features:")
print("*******************************************************************")
print(features_non_infected[:5])


# feature to index mapping
feature_index_map = {}
counter = 0

for feature_row in features_infected:
    for feature in feature_row:
        if feature not in feature_index_map:
            feature_index_map[feature] = counter
            counter = counter + 1
            
for feature_row in features_non_infected:
    for feature in feature_row:
        if feature not in feature_index_map:
            feature_index_map[feature] = counter
            counter = counter + 1
            

# feature vector
def features_to_vector(features, cls):
    row = np.zeros(len(feature_index_map) +1 ) # last column is for the class attribute, 1= infected, 2 = noninfected
    for f in features:
        index = feature_index_map[f]
        row[index] = 1
        #@todo normalization, if that helps 
        row[-1] = cls
    return row
        
data_feature_vector = np.zeros(((len(features_infected) + len(features_non_infected)), (len(feature_index_map) + 1)))


row_count =0
for feature_row in features_infected:
    vector = features_to_vector(feature_row, 1) # 1 =  infected
    data_feature_vector[row_count, :] = vector
    row_count = row_count + 1
    
for feature_row in features_non_infected:
    vector = features_to_vector(feature_row, 0) # o = non infected
    data_feature_vector[row_count, :] = vector
    row_count = row_count + 1


print("*******************************************************************")
print("feature vector:")
print("*******************************************************************")


data_feature_vector_df = pd.DataFrame(data_feature_vector)
path = os.path.join(folder_path_result, "feature_vector.csv")
data_feature_vector_df.to_csv(path, sep=',')
print(data_feature_vector_df[:5])

feature_index_map_list = []
for key, val in feature_index_map.items():
    temp = [val,key]
    feature_index_map_list.append(temp)

#last colums is the class
temp = [len(feature_index_map_list), "class"]
feature_index_map_list.append(temp)

feature_index_map_df = pd.DataFrame(feature_index_map_list, columns = ['idx', 'feature'])
path = os.path.join(folder_path_result, "feature_vector_index_map.csv")
feature_index_map_df.to_csv(path, sep=',', index = False)

print("*******************************************************************")
print("feature index map (showing first 50):")
print("*******************************************************************")
print(feature_index_map_list[:50])

print("\n\nDone with preprocessing. Now you can run the code file for individual Machine Learning Algorithms.")
