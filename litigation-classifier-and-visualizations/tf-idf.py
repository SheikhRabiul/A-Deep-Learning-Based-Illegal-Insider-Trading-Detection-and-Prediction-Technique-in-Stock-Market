# -*- coding: utf-8 -*-
"""
Created on 2017
Modified on Thu Jul  5 14:47:35 2018
Purpose: TF-IDF for feature ranking. 
Prerequisite: please run the preprocessing script (preprocessing_alt.py) for this algorithm first.
@author: Dr. Chen & Dr. Robert Bridges
@modified by: Sheikh Rabiul Islam ; sislam42@students.tntech.edu

"""
#import modules
import os
import pandas as pd
import numpy as np
from generalFunctions import *
from functions import *

folder_path_result = "result/"
file_name = "feature_vector_index_map.csv"
f_path = os.path.join(folder_path_result, file_name)
features_df = pd.read_csv(f_path, index_col=0)
features_df = features_df[:-1]  # drop last row (class)
features_list = features_df['feature'].values.tolist()

file_name = "X.csv"
f_path = os.path.join(folder_path_result, file_name)
feature_vector_infected = pd.read_csv(f_path, index_col=0)

file_name = "Y.csv"
f_path = os.path.join(folder_path_result, file_name)
feature_vector_non_infected = pd.read_csv(f_path, index_col=0)

X = feature_vector_infected.values
Y = feature_vector_non_infected.values
   
def tf_idf(X, Y):
    tf = np.sum(X, axis=0)
    df = np.sum(np.where(Y > 0, 1, 0), axis=0)
    N = Y.shape[0] + 1  ## num of docs + 1
    idf = -np.log((df + 1) / float(N))

    return tf * idf


l = tf_idf(feature_vector_infected, feature_vector_non_infected)

tfidf_indicative_features = sorted( [( features_list[i], l[i] ) for i in range(len(l)) ] , key = lambda x:x[1], reverse = True)

print (len(tfidf_indicative_features))


df_result_rfc = pd.DataFrame(tfidf_indicative_features,columns=['feature','score'])
df_result_rfc.insert(1,"scaled_score", scale_a_list(df_result_rfc['score'],0,1))
print("top 5 features using tf-idf:")
print(df_result_rfc.head())
output_folder = "result/"
f_name = 'feature_vector_index_map_tf_idf.csv'
f_path = os.path.join(output_folder, f_name)
print("saving  ranked features in ")
print(f_path)
df_result_rfc.to_csv(f_path, sep=',')
