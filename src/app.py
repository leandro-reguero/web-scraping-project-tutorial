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
        print(html_data)

    else:
        print(f"There was an error with code: {response.status_code}")

get_scraped()

# table data (td) sin class = date
# table data (td) class text-right = value

# div row, div col-6, table table

