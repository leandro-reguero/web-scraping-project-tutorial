import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import re


# Defining the GET function to start scraping
def get_scraped():
    global url
    url = 'https://ycharts.com/companies/TSLA/revenues'
    # User-Agent 
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
               }
    
    # GET Request with User-Agent 
    response = requests.get(url, headers=headers)
    time.sleep(9)
    if response.status_code == 200:
        html_data = response.text
        print(html_data)

    else:
        print(f"There was an error with code: {response.status_code}")


get_scraped()
