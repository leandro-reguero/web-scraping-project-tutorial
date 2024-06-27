import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import re
from numpy import random
import numpy as np
import pandas as pd



# Defining the GET function to start scraping
def get_scraped():
    global url
    url = 'https://ycharts.com/companies/TSLA/revenues'

    # User-Agent rotation
    user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
    ]
    for i in range(1, 4):
        user_agent = random.choice(user_agent_list)

    headers = {'User-Agent': user_agent}
    
    # GET Request with User-Agent choice
    response = requests.get(url, headers=headers)
    time.sleep(9)
    if response.status_code == 200:
        html_data = response.text
        global soup
        soup = BeautifulSoup(response.content, 'html.parser')

    else:
        print(f"There was an error with code: {response.status_code}")

get_scraped()

v_list = []
d_list = []
tables = soup.find_all('table', class_='table')


dates = tables[0].find_all('td', class_=None) + tables[1].find_all('td', class_=None)
values = tables[0].find_all('td', class_='text-right') + tables[1].find_all('td', class_='text-right')


for value in values:
    v_list.append(value.text.strip())

for date in dates:
    d_list.append(date.text.strip())

# Creando el DataFrame
dicto = {'Date': d_list, 'Value': v_list}
df = pd.DataFrame(dicto)

#Procesando y limpiando el DataFrame
df['Date'] = pd.to_datetime(df['Date'])
in_b = {'M': '*0.001', 'B': ''}
df['Value'] = df['Value'].replace(in_b, regex=True).map(pd.eval).round(3)

print(df)

