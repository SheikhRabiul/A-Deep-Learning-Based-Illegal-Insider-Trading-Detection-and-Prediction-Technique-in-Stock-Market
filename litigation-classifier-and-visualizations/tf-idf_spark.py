# run this command from your spark home folder to run this script:  spark-submit tf-idf_spark
from __future__ import print_function
import numpy
from pyspark import SparkContext
import csv
from pyspark.mllib.feature import HashingTF, IDF
if __name__ == "__main__":
    sc = SparkContext(appName="TFIDFExample")  
    documents = sc.textFile("spark_input.txt").map(lambda line: line.split(" "))
    hashingTF = HashingTF()
    tf = hashingTF.transform(documents)
    tf.cache()
    idf = IDF().fit(tf)
    tfidf = idf.transform(tf)
    file = open("result/spark_output.txt","w")   
    for each in tfidf.collect():
        file.write(repr(each))
        #print(each)
        #from the position of the element try to find out the actual word, this part can be automated too. 
    file.close() 
    print("Done")
    sc.stop()
