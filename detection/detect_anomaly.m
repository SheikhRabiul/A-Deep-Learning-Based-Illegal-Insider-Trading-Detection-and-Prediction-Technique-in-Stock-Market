% Author: Sheikh Rabiul Islam
% Date: 11/20/2017
% Purpose: Discrete singal( time series) similarity measures
close all

%global variables
global window_size;
global actual_data;
global predicted_data_window_based;
global predicted_data_day_based;
global predicted_data_historical_based;
global pattern_desc_arr;
global pattern_mat;
global overlap;
global result;
result =[];


% configure this as needed
num_method = 3;
num_pattern = 11;
window_size = 50;
overlap = 10;


%load data
actual_data = csvread('input/bp_full_window_act.csv');
predicted_data_window_based = csvread('input/bp_full_window_pred.csv');
predicted_data_day_based = csvread('input/bp_full_point_pred.csv');
predicted_data_historical_based = csvread('input/bp_full_sequence_pred.csv');
pattern_mat = csvread('input/pattern.csv');
pattern_desc_arr = csvread('input/pattern_sizes.csv');



methods = [length(predicted_data_window_based), ceil(length(predicted_data_window_based)/ window_size);
    length(predicted_data_day_based), ceil(length(predicted_data_day_based)/ window_size);
    length(predicted_data_historical_based), ceil(length(predicted_data_historical_based)/ window_size)
    ];



for method = 1:3
    %%for each method
    num_window = methods(method,2);
    for window = 1:num_window
        %%for each window
        normalized_cross_correlation(method, window, 0, 0);
        for pattern = 1:num_pattern
            %%for each pattern
            overlap = 10;
            if window == num_window
                overlap = 0;
            end
            for day = 1:( window_size - ( pattern_desc_arr(pattern) - overlap))
                %%for each sliding window of size pattern
                normalized_cross_correlation(method, window, pattern, day);
                %%normalized_cross_correlation(method, window, pattern, day)
            end
        end
    end
end

% write result
csvwrite('output/bp_output.csv',result)
% print result matrix
result_header = 'Method, Window, Pattern, Day'
result 

function normalized_cross_correlation(method, window, pattern, day) 
    signal1 = [];
    signal2 = [];
    predicted_data = [];
    graph_title1= '';
    graph_title2 = '';
    global predicted_data_window_based;
    global predicted_data_day_based;
    global predicted_data_historical_based;
    global window_size;
    global actual_data;
    global pattern_desc_arr;
    global pattern_mat;
    global overlap;
    global result;
    
    if method == 1  
        predicted_data = predicted_data_window_based(:,:);
        graph_title1 = 'True vs predicted (window based).(w=';
        graph_title1 =[graph_title1  int2str(window)  ',p ='  int2str(pattern)  ',d=' int2str(day)  ')'];
        graph_title2 = 'Day lag vs normalized cross correlation.(w=';
        graph_title2 =[graph_title2  int2str(window)  ',p=' int2str(pattern) ',d=' int2str(day) ')'];
    elseif method == 2
        predicted_data = predicted_data_day_based(:,:);
        graph_title1 = 'True vs predicted (day based).(w=';
        graph_title1 =[graph_title1  int2str(window)  ',p ='  int2str(pattern)  ',d=' int2str(day)  ')'];
        graph_title2 = 'Day lag vs normalized cross correlation.(w=';
        graph_title2 =[graph_title2  int2str(window)  ',p=' int2str(pattern) ',d=' int2str(day) ')'];
    elseif method == 3
        predicted_data = predicted_data_historical_based(:,:);
        graph_title1 = 'True vs predicted (whole historical based).(w=';
        graph_title1 =[graph_title1  int2str(window)  ',p ='  int2str(pattern)  ',d=' int2str(day)  ')'];
        graph_title2 = 'Day lag vs normalized cross correlation.(w=';
        graph_title2 =[graph_title2  int2str(window)  ',p=' int2str(pattern) ',d=' int2str(day) ')'];
    end
            
    if pattern == 0    % %actual vs predicted checking; no comparison with anomalous pattern
        signal1_start = ((window-1) * window_size) +1;
        signal1_end = signal1_start + window_size -1;
        if length(predicted_data) < signal1_end
            signal1_end = length(predicted_data);
        end
        signal2_start = signal1_start;
        signal2_end = signal1_end;
        
        signal1 = predicted_data(signal1_start : signal1_end);
        signal2 = actual_data(signal2_start: signal2_end);
    elseif pattern > 0 % comparison involves anomalous pattern and any of predicted or actual data.
        
        signal1_start = ((window-1) * window_size) + day;
        signal1_end = signal1_start + pattern_desc_arr(pattern)-1;
        if length(predicted_data) < signal1_end
            signal1_end = length(predicted_data);
        end
        signal1 = predicted_data(signal1_start : signal1_end);
        signal2 = pattern_mat(pattern,1: pattern_desc_arr(pattern));
        signal2 = signal2.';
    end
    
    if length(signal1) == length(signal2)
        %
        [cor_sequence,lag] = xcorr(signal1,signal2, 'coeff');
        if max(cor_sequence) > .80
            result = [result; method window pattern day];
            x1=linspace(1,length(signal1),length(signal1));
            figure()
            plot(x1,signal2,x1,signal1)
            legend('actual','predicted')
            xlabel('day')
            ylabel('volume')
            title(graph_title1);

            figure()
            plot(lag, cor_sequence)
            [max_cor,max_index] = max(cor_sequence);

            xlabel2 = ['Maximum ncr = ' num2str(max_cor) ' at day lag = ' int2str(lag(max_index))];
            xlabel({'day lag',xlabel2})
            ylabel('normalized cross correlation')
            title(graph_title2);
        end
    end
    
    
end



 