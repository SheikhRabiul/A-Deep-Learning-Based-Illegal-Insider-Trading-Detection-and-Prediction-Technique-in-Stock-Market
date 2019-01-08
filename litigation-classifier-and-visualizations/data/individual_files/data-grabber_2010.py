# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd

start = 21358
##
#end = 18530
end = 21796
year = 2010
exclude = []

data_df = pd.DataFrame(columns=['lt_no','yr','title', 'lt'])
for i in range(start, end):
    print("processing  ", i)
    if i not in exclude:
        
        url = "https://www.sec.gov/litigation/litreleases/"  + str(year) +  "/lr" + str(i) + ".htm"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        header = soup.findAll("h2")
        #print(header)
        if  header:
            header = str(header)
            header = (header.replace("'","")).replace("\"","")
            
            content = soup.find_all("p")
            #print(content)
            if content:
                #content =  content
                content = (((str(content)).replace("\"","")).replace("'","")).replace("\n","")
                content = content.replace("<p>", "")
                content = content.replace("</p>", "")
                #print(content)
                row_dict = {'lt_no': i, 'yr': year, 'title': header, 'lt': content}
                data_df=data_df.append(row_dict, ignore_index = True)

file_name = str(year) + ".csv"
data_df.to_csv(file_name, encoding='utf-8', index=False)

