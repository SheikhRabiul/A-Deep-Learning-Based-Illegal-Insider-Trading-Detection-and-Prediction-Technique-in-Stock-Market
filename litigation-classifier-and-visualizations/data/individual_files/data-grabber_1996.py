# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from lxml import html 
import pandas as pd

start = 14770
##
#end = 18530
end = 15203
year = 1996
exclude = []

data_df = pd.DataFrame(columns=['lt_no','yr','title', 'lt'])
for i in range(start, end):
    print("processing  ", i)
    if i not in exclude:
        
        url = "https://www.sec.gov/litigation/litreleases/lr" + str(i) + ".txt"
        page = requests.get(url)
        content = str(page.content)
        content = content.replace("\"","")
        content = content.replace("'","")
        content = content.replace("\\n","")
        header = ""
        row_dict = {'lt_no': i, 'yr': year, 'title': header, 'lt': content}
        data_df=data_df.append(row_dict, ignore_index = True)

file_name = str(year) + ".csv"
data_df.to_csv(file_name, encoding='utf-8', index=False)

