import pandas as pd
import re
data_df = pd.read_csv('data/complete_dataset.csv')

count =0
count2 =0
both = 0
anyone =0
data_df['class'] = 0
for index, row in data_df.iterrows():
    title_flag= False
    litigation_flag = False
    title = str(row['title'])
    litigation = str(row['lt'])
    if 'insider' in title.lower():
        #print(count)
        #print(title)
        count +=1
        anyone +=1
        title_flag = True
        data_df.loc[index,'class'] = 1
        
    if 'insider' in litigation.lower():
        #print(count2)
        #print(title)
        count2 +=1
        anyone +=1
        litigation_flag = True
        data_df.loc[index,'class'] = 1
        
    if title_flag and litigation_flag:
        both+=1
        
print("In title:", count)
print("In body:", count2)
print("In anyone:", anyone - both)
print("In both:", both)

data_infected_df = data_df[data_df['class'] ==1]
data_non_infected_df = data_df[data_df['class'] ==0]

data_infected_df.pop('Unnamed: 0')
data_non_infected_df.pop('Unnamed: 0')

data_infected_df.to_csv("data/infected/infected.csv", sep=',')
print("saving infected file in data/infected/infected.csv")
data_non_infected_df.to_csv("data/non_infected/non_infected.csv", sep=',')
print("saving infected file in data/non_infected/non_infected.csv")