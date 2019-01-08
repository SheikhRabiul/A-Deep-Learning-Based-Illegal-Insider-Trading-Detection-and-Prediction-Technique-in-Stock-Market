
"""
Date: 
Purpose: 
Author : Sheikh Rabiul Islam
Email: sislam42@students.tntech.edu
"""

import math
import csv
import pandas as pd
from textblob import TextBlob as tb

# scale a number from a range to a different range (eg. 1..100 to 0 ..1)
def scale_a_number(inpt, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(inpt-from_min)/(from_max-from_min)+to_min

# calculate term frequency (number of times as word appear in a document/record), tfidf calculation code template is taken from  http://stevenloria.com/finding-important-word-in-a-document-using-tf-idf
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)
    
# number of document/record contains the word
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)
    
# inverse document frequency which measures how common a word is among all documents/ records
def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

#product of tf and idf which computes TF-IDF score
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# load credit card usage categories data
df = pd.read_csv('data/infected/infected.csv')

# store the data in a bloblist
bloblist = []

for index,row in df.iterrows():
    bloblist.append(tb(str(row[3]) + str(row[4])))

#for each customer calculate most important 5 words based on credit card usage category list. 
df_result = pd.DataFrame(columns=['word', 'score'])

for i, blob in enumerate(bloblist):
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    res_str = ''
    for word, score in sorted_words:
        #tmp_str =  " | %s:%s" % (word,round(score,4))
        #res_str += tmp_str
        row = {'word': word, 'score': score }
        #print(row)
        df_result = df_result.append(row, ignore_index=True)
    #res_str += ' | '    
    #df_result.set_value(i,'gift_choice_hints',res_str)
df_result = df_result.sort_values('score',ascending=False)
df_result = df_result.iloc[:20, :]
df_result.to_csv("result/tfidf.csv", index=False)