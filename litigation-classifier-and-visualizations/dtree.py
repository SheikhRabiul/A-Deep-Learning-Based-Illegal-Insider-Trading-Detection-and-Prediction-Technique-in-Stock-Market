# -*- coding: utf-8 -*-
"""
Created on June, 2018
@created by: Sheikh Rabiul Islam ; sislam42@students.tntech.edu
Purpose: Classifying malware logs and visualizing samples in an intuitive manner.
"""
# load needed classes
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import graphviz 
import pydotplus
import pandas as pd
import collections
import numpy as np

#input files
# append _ft or _rf or _rfmda at the end of file name; 
# _ft means we want to use the features selected by Forest of Trees algorithms here..in th same way..rf= random forest, rfmda= random forest with meand decrease accuracy

#balanced feature selection
file_data = "result/feature_vector_final_et_balanced.csv"
file_features = "result/feature_vector_index_map_final_et_balanced.csv"

#biased
#file_data = "result/feature_vector_final_et.csv"
#file_features = "result/feature_vector_index_map_final_et.csv"


#output folder
output_folder = "result/"

dataset = pd.read_csv(file_data, index_col=0)
features_df = pd.read_csv(file_features, index_col=0)
features = features_df['feature'].tolist()
features.pop()
classes = ['non-infected', 'infected']

X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=35, test_size = .3, shuffle = True)
print (dataset.head())


#balanced
#clf = DecisionTreeClassifier(max_depth=35,min_samples_leaf=2,min_samples_split=2, class_weight='balanced')
#biased
clf = DecisionTreeClassifier(max_depth=35,min_samples_leaf=2,min_samples_split=2, class_weight={0:.9999, 1:.0001})
clf.fit(X_train,y_train)

print("showing prediction results (first 10) [1=infected, 0 = non infected]:")
y_pred = clf.predict(X_test)
print(y_pred[:5])
a = X_test[:1]

print("a:")
print(a)

#print('sk_pred: {}'.format(clf.predict(a)))
#print('true: {}'.format(y_test[:3]))

# shows the end point of the tree traverse by a sample
print("Returns the index of the leaf that each sample is predicted as:")
index_of_leaf = clf.apply(a)
print(index_of_leaf)


#decision path shows the nodes of the tree that were traverse by the sample.
print("decision path:")
d_path = clf.decision_path(a)
print(d_path)

print("nodes in the decision path:")
n_d_path = np.unique(np.sort( d_path.indices))
print(n_d_path)


print("probability of each class:")
print(clf.predict_proba(a))

print("Feature importances:")
feature_importances = clf.feature_importances_
print(feature_importances)



#accuracy -number of instance correctly classified
acsc = accuracy_score(y_test, y_pred) 
print("accuracy (percentage  of instance classified correctly):")
print(acsc)


print("confusion matrix:")
cm = confusion_matrix(y_test, y_pred)
df_cm = pd.DataFrame([[cm[1][1], cm[0][0],cm[0][1], cm[1][0]]], 
                        index=[0],
                        columns=['True Positives','True Negatives', 'False Positives', 'False Negatives'])
print(df_cm)

#precision, recall, fscore, support
precision, recall, fscore, support = precision_recall_fscore_support(y_test, y_pred,average='binary')

df_metrics = pd.DataFrame([[acsc, precision, recall, fscore]], 
                        index=[0],
                        columns=['accuracy','precision', 'recall', 'fscore'])
print(df_metrics)
#dot_data = tree.export_graphviz(clf, out_file=None) 
#graph = graphviz.Source(dot_data)

dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=features,  
                         class_names=classes,  
                         filled=True, rounded=True,  
                         special_characters=True)


graph = graphviz.Source(dot_data)
graph.render("wannacry")


# Draw graph
graph = pydotplus.graph_from_dot_data(dot_data)  

# Show graph
graph.write_pdf("wannacry_rfc.pdf")

#draw the traversal path

color = 'red'
edges = collections.defaultdict(list)

for edge in graph.get_edge_list():
    edges[edge.get_source()].append(int(edge.get_destination()))

for edge in edges:
    edges[edge].sort()  
    for i in range(2):
        dest = graph.get_node(str(edges[edge][i]))[0]
        if edges[edge][i] in n_d_path:
            dest.set_fillcolor(color)
graph.write_png('sample_rfc.png')

