# code in this folder is not well organized; this code is the customized version of another project of mine. So
# there might be some unnecessary files or code snipped..
# If you read my paper on this then I guess you will able to figure out what portion exactly you need.
# here is the paper that I presented in IEEE Big Data 2018 conference: https://arxiv.org/pdf/1807.00939.pdf

# requires  graphviz, pydotplus and pandas modules

# procedure 1
  step 1: preprocess the data
	     python preprocess.py
  step 2: rank features and discard insignificant features [currently 3 different ways]
	     python feature_selection.py
  step 3: update feature vector 
	     python update feature vector
  step 4: try individual Machine Learning algorithms 
	     python dtree.py 


# procedure 2
  step 1: try individual Machine Learning algorithms
	    python dtree.py

#output
generated tree - viz****
visualizing how a sample traverse the tree and mark them as red to mark the common path - sample.png


#running tf-idf

    step 1: preprocess the data
            python preprocess_alt.py
    step 2: run feature selection algorithms
            python lda.py
            python tf-idf.py