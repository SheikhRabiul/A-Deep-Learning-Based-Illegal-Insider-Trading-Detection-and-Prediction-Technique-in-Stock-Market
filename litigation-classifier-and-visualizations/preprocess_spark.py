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

file = open("result/spark_input.txt","w",  encoding="utf-8")  
for feature_row in features_infected:
    str1 = ' '.join(feature_row)
    file.write(str1) 
file.close() 

print("output written to result/spark_input.txt")

#file = open(“testfile.txt”,”w”) 
 
#file.write(“Hello World”) 
