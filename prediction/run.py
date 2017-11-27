# Code template by Jakob Aungiers 
# Modified by: Sheikh Rabiul Islam
# Date: 11/10/2017 
# Purpose : stock market volatility prediction
import lstm
import time
import matplotlib.pyplot as plt
import pandas as pd
import csv
import itertools

def plot_results(predicted_data, true_data,method,dataset,company):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    df_pr = pd.DataFrame(predicted_data)
    fname = 'output/' + company + '_' + dataset + '_' + method + '_pred.csv' 
    df_pr.to_csv(fname, index=False, header=False)
    df_tr = pd.DataFrame(true_data)
    fname = 'output/' + company + '_' + dataset + '_' + method + '_true.csv'
    df_tr.to_csv(fname, index=False, header=False)

    plt.show()

def plot_results_multiple(predicted_data, true_data, prediction_len,method,dataset,company):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    pr_list=[]
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        pr_list.append(data)
        plt.legend()
    pr_list_flat = list(itertools.chain.from_iterable(pr_list)) # converting a list of list in to a 1-d list
    df_pr = pd.DataFrame(pr_list_flat)
    fname = 'output/' + company + '_' + dataset + '_' + method + '_pred.csv'
    df_pr.to_csv(fname, index=False, header=False)
    df_tr = pd.DataFrame(true_data)
    fname = 'output/' + company + '_' + dataset + '_' + method + '_act.csv'
    df_tr.to_csv(fname, index=False, header=False)
    plt.show()
    

#Main Run Thread
if __name__=='__main__':
	global_start_time = time.time()
	epochs  = 1   # changing epoc to larger values helps getting better prediction.
	seq_len = 50

	company='gtxi'   #company_code
	method='window'	# window, sequence, point
	dataset='partial'   # full, partial


	print('> Loading data... ')

	fname = 'input/' + company + '_' + dataset + '.csv'
	X_train, y_train, X_test, y_test = lstm.load_data(fname, seq_len, True)

	print('> Data Loaded. Compiling...')

	model = lstm.build_model([1, 50, 100, 1])

	model.fit(
	    X_train,
	    y_train,
	    batch_size=512,
	    nb_epoch=epochs,
	    validation_split=0.05)
	fig_name = company + '_' + dataset + '_' + method	
	print(fig_name)	

	if method == 'window':
		predictions = lstm.predict_sequences_multiple(model, X_test, seq_len, 50)
		print('Training duration (s) : ', time.time() - global_start_time)
		plot_results_multiple(predictions, y_test, 50, method, dataset, company)

	if method == 'sequence':
		predictions = lstm.predict_sequence_full(model, X_test, seq_len)
		print('Training duration (s) : ', time.time() - global_start_time)
		plot_results(predictions, y_test, method, dataset, company)

	if method == 'point':
		predictions = lstm.predict_point_by_point(model, X_test) 
		print('Training duration (s) : ', time.time() - global_start_time)
		plot_results(predictions, y_test, method, dataset, company)
