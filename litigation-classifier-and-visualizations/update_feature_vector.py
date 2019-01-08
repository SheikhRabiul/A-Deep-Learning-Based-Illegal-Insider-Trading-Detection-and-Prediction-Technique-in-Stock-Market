# -*- coding: utf-8 -*-
"""
Created on June, 2018
@created by: Sheikh Rabiul Islam ; sislam42@students.tntech.edu
Purpose: update feature vector based on the selected (discarding features that has no significant effect) features.
"""
# load needed classes

import pandas as pd
import numpy as np
import os

#input files
file_feature_vector = "result/feature_vector.csv"
file_feature_index_map = "result/feature_vector_index_map.csv"

#balanced
file_selected_features = ["result/feature_vector_index_map_filtered_rfc_balanced.csv", "result/feature_vector_index_map_filtered_et_balanced.csv"]
#biased
#file_selected_features = ["result/feature_vector_index_map_filtered_rfc.csv", "result/feature_vector_index_map_filtered_et.csv"]

#output folder
output_folder = "result/"
#balanced
file_updated_feature_vector = ["result/feature_vector_final_rfc_balanced.csv", "result/feature_vector_final_et_balanced.csv"]
#biased
#file_updated_feature_vector = ["result/feature_vector_final_rfc.csv", "result/feature_vector_final_et.csv"]


for j in range(1,2):
    feature_vector_df = pd.read_csv(file_feature_vector, index_col=0)
    feature_index_map = pd.read_csv(file_feature_index_map, index_col=0)
    feature_index_map_selected = pd.read_csv(file_selected_features[j], index_col=0)
    
    data_feature_vector = np.zeros(((len(feature_vector_df) ), (len(feature_index_map_selected) + 1)))
    for i in range(len(feature_index_map_selected)):
        #grab the old index of the feature
        feature = feature_index_map_selected.loc[i,'feature']
        #print(feature_index_old_row)
        feature_index_old = feature_index_map[feature_index_map['feature']==feature].index.item()
        data_feature_vector[:,i] = feature_vector_df.iloc[:, feature_index_old]
        
    #copy last attribut (class)    
    data_feature_vector[:,len(feature_index_map_selected)]= feature_vector_df.iloc[:, len(feature_index_map)-1]    
    data_feature_vector_df = pd.DataFrame(data_feature_vector)
    print("first few updated feature vector")
    print(data_feature_vector_df.head())
    print("saving in ..")
    print(file_updated_feature_vector[j])
    data_feature_vector_df.to_csv(file_updated_feature_vector[j], sep=',')    
    
    
