# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:03:37 2018
@created by: Sheikh Rabiul Islam
Purpose: preprocess the data so that it can be feeded in to Machine Learning Alogorithms.This preprocess is required for LDA and TF-IDF that comes from the old project
"""
# configure folder path here
folder_path_infected = "data/infected/"
folder_path_non_infected = "data/non_infected/"
folder_path_result = "result/"
folder_path_result_interim = "result/interim/"

#import modules
import os
import pandas as pd
import numpy as np
from generalFunctions import *
from functions import *


#global containers
features = []
feature_vector_infected = []
feature_vector_non_infected = []

#list of words that we do not want to consider as feature
stopwords = set(w.rstrip() for w in open('stopwords.txt'))
wildcards = set(w.rstrip() for w in open('wildcards.txt'))

file_name = "result/feature_vector_index_map.csv"
features_df = pd.read_csv(file_name, index_col=0)
features_df = features_df[:-1]  # drop last row (class)

features_list = features_df['feature'].values.tolist()

features_dict = {row['feature']: index for index, row in features_df.iterrows()}

#for index,row in features_df.iterrows():
#    features_dict.add(row['feature'],index)

file_name = "result/feature_vector.csv"
#features_vector_df = pd.read_csv(file_name, index_col=0)

#number of files in infected directory
infected_files_count = 0
for filename in os.listdir(folder_path_infected):
    if filename.endswith('.json'):
        infected_files_count += 1

#number of files in noninfected directory
non_infected_files_count = 0
for filename in os.listdir(folder_path_non_infected):
    if filename.endswith('.json'):
        non_infected_files_count += 1


# X
feature_vector_infected = pd.DataFrame(0, index = range(infected_files_count), columns = range(len(features_df)))
# Y 
feature_vector_non_infected = pd.DataFrame(0, index = range(non_infected_files_count), columns = range(len(features_df)))

def build_feature_vector(folder, wls, document_serial):
    # list of tags in the log file that we are interested
    interested_keys = ["data_object","data_content","data_regkey","data_file", "event", "object", "api", "arguments_1_value", "category"]

    for i in range (0,len(wls)):
        for key, val in wls[i].items():
            val = str(val).lower()
            val = "%r"%val #converting into raw string
            if key in interested_keys: 
                
                # check whether the value for the features is atleast 3 character and the value is not in the list of stopwords;
                # stopwords is a list of words that usually doesn't help. i.e., prepositions.
                if len(val)>2 and len(val)<200 and val not in stopwords:
                    #check if more than 2 / exists; if so then keep only the first and last one
                    #check for null rows 
                    #check for \n characters
                    val = os.path.normpath(val)
                    val_l = val.split(os.sep)
                    
                    if len(val_l)>1:
                        val = val_l[0]+val_l[len(val_l)-1]
                        #print(new_s)
                    
                    # check for extensions ; i.e., XXXXXXXXX.wnry could be replaced with %.wnry
                    keyword = ''
                    for e in wildcards:
                        if val.endswith(e):
                            val_temp = val[0:5]+ '*' + e
                            keyword = key + "+" + val_temp                        
                        else:
                            keyword = key + "+" + val
                    #check if the keyword is in featues
                    index = features_dict[keyword]
                    if folder == "infected":
                        feature_vector_infected.iloc[document_serial][index] += 1
                    else:
                        feature_vector_non_infected.iloc[document_serial][index] += 1
    #no return value


print("*******************************************************************")
print ("Populating feaure vector from infected logs ... ")
print("*******************************************************************")
document_serial = 0
for filename in os.listdir(folder_path_infected):
    if filename.endswith('.json'):
        print ("starting file %s ... " % filename)
        path = os.path.join(folder_path_infected, filename)
        wls = unjsonify(path)  ## list of dicts
        try:
            folder ='infected'
            build_feature_vector(folder, wls,document_serial)
            document_serial = document_serial + 1
            print("\n")
        except:
            pass

print("*******************************************************************")
print ("Populating features from the non infected logs (showing first 5) ... ")
print("*******************************************************************")
document_serial = 0
for filename in os.listdir(folder_path_non_infected):
    if filename.endswith('.json'):
        print ("starting file %s ... " % filename)
        path = os.path.join(folder_path_non_infected, filename)
        wls = unjsonify(path)  ## list of dicts
        try:
            folder ='infected'
            build_feature_vector(folder, wls,document_serial)
            document_serial = document_serial + 1 
            print("\n")
        except:
            pass



output_folder = "result/"
f_name = 'X.csv'
f_path = os.path.join(output_folder, f_name)
print("saving X in ")
print(f_path)
feature_vector_infected.to_csv(f_path, sep=',')


f_name = 'Y.csv'
f_path = os.path.join(output_folder, f_name)
print("saving Y in ")
print(f_path)
feature_vector_non_infected.to_csv(f_path, sep=',')

