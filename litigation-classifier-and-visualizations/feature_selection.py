# -*- coding: utf-8 -*-
"""
Created on June, 2018
@created by: Sheikh Rabiul Islam ; sislam42@students.tntech.edu
Purpose: selecting important features that contributes in the classifying process.
"""
# load needed classes
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score, ShuffleSplit
from collections import defaultdict
from sklearn.metrics import r2_score
from functions import *
import pandas as pd
import numpy as np
import os
#configure here
selected_algorithm =1 # 1= extra trees, 2 = random Forest
biased = True    # make it false if you want it balanced
threshold_feature_score = 0

#input files
file_data = "result/feature_vector.csv"
file_features = "result/feature_vector_index_map.csv"

#output folder][]]][[[[o]]]]]
output_folder = "result/"

dataset = pd.read_csv(file_data, index_col=0)
features_df = pd.read_csv(file_features, index_col=0)
features = features_df['feature'].tolist()
features.pop()
classes = ['non-infected', 'infected']

X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values


print("******************* starting feature ranking process ********************")

if selected_algorithm == 1:
    ############ Extra Trees Classifiers
    #balanced
    forest = ExtraTreesClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=False, oob_score=False, n_jobs=10, random_state=None, verbose=0, warm_start=False, class_weight='balanced')
    #biased to malicious class
    if biased:
        forest = ExtraTreesClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=False, oob_score=False, n_jobs=10, random_state=None, verbose=0, warm_start=False, class_weight={0:.9999,1:.0001})
    
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
	

	
    data= (sorted(zip(map(lambda x: round(x, 4), forest.feature_importances_), features),reverse=True))
    #converting the list to a datafreame
    df_result_et = pd.DataFrame(data,columns=['score','feature'])
    df_result_et.insert(1,"scaled_score", scale_a_list(df_result_et['score'],0,1))
    print("top 5 features using Extra Trees:")
    print(df_result_et.head())
    f_name = 'feature_vector_index_map_et_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  ranked features in ")
    print(f_path)
    df_result_et.to_csv(f_path, sep=',')

############ Random Forest Classifier)
if selected_algorithm == 2:
    #balanced
    forest = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=4, random_state=None, verbose=0, warm_start=False, class_weight='balanced')
    #biased
    if biased:
        forest = RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=4, random_state=None, verbose=0, warm_start=False, class_weight={0:.9999,1:.0001 })
    
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
    data= (sorted(zip(map(lambda x: round(x, 4), forest.feature_importances_), features),reverse=True))
    #converting the list to a datafreame
    df_result_rfc = pd.DataFrame(data,columns=['score','feature'])
    df_result_rfc.insert(1,"scaled_score", scale_a_list(df_result_rfc['score'],0,1))
    print("top 5 features using Random forest classifier:")
    print(df_result_rfc.head())
    f_name = 'feature_vector_index_map_rfc_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  ranked features in ")
    print(f_path)
    df_result_rfc.to_csv(f_path, sep=',')
    
print("******************* ending feature selection ********************")


print("\n ******************* discarding  insignificant features (score 0) ********************")

if selected_algorithm == 1:    
    df_result_et_new = df_result_et[df_result_et['scaled_score']>0]
    f_name = 'feature_vector_index_map_filtered_et_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  filtered features index map  in ")
    print(f_path)
    df_result_et_new.to_csv(f_path, sep=',')
    
if selected_algorithm == 2:
    df_result_rfc_new = df_result_rfc[df_result_rfc['scaled_score']>0]
    f_name = 'feature_vector_index_map_filtered_rfc_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  filtered features index map  in ")
    print(f_path)
    df_result_rfc_new.to_csv(f_path, sep=',')

print("\n ****************** updating feature index maping file ***********************")

if selected_algorithm == 1:
    df_result_et_new.pop('score')
    df_result_et_new.pop('scaled_score')
    df_result_et_new = df_result_et_new.append(pd.DataFrame(['class'],columns = ['feature']), ignore_index = True)
    f_name = 'feature_vector_index_map_final_et_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  updated features in ")
    print(f_path)
    df_result_et_new.to_csv(f_path, sep=',')

if selected_algorithm == 2:
    df_result_rfc_new.pop('score')
    df_result_rfc_new.pop('scaled_score')
    df_result_rfc_new = df_result_rfc_new.append(pd.DataFrame(['class'],columns = ['feature']), ignore_index = True)
    f_name = 'feature_vector_index_map_final_rfc_balanced.csv'
    f_path = os.path.join(output_folder, f_name)
    print("saving  updated features in ")
    print(f_path)
    df_result_rfc_new.to_csv(f_path, sep=',')
