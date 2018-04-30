###### Author: Hitesh Sahadeo Chache 
# 
#  Jupyter Link: https://github.com/hchache/Data-Incubator-Challenge/blob/master/Question%203.ipynb
#  
###### Code - Start

import pandas as pd
import numpy as np
import math as m
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import string
from pandas.io.json import json_normalize


# Kaggle dataset
import json
with open('full_format_recipes.json') as json_data:
    d = json.load(json_data)

df = pd.DataFrame.from_dict(json_normalize(d), orient='columns')
df.iloc[140]


# This was only for pancake recipes. Same code can be used for all other recipes.
title_col = df['title']
pan_cake = []
pc_index = []
for i,t in enumerate(title_col):
    if 'Pancake' in str(t):
        pc_index.append(i)

pc_index = df.iloc[pc_index]
a = pc_index['ingredients']
b = []
for row in a:
    if len(row):
        for i in range(len(row)):
            b.append(row[i].split(","))


pancake_words= []
ingred.remove("Tea")
for text in b:
#     print(text[0])
    for word in ingred:
        if word.lower() in text[0].lower():
            pancake_words.append(word)
# print(pancake_words)
from collections import Counter
counts = Counter(pancake_words)
print(counts)

# This code generates list of possible ingredients from bbc.com
# This code was rewritten on existing code

ingred = []
def get_ingredients(soup):
    lists = soup.findAll('li',{'class':'resource food'})
#     print(lists)
    array = []
    for li in lists:
        ingred.append(li.a.contents[2].strip())

a_to_z = string.ascii_lowercase[:26]
for a in a_to_z:
    url = 'https://www.bbc.com/food/ingredients/by/letter/' + a
    req = requests.get(url, headers={'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    get_ingredients(soup)


# Generate CSV file, which will be used in web application
df = pd.DataFrame.from_dict(counts, orient='index').to_csv('pancake.csv', index=True, header=["value"],index_label=["id"])

