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
from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv



# definiendo la funcion del GET request para scrapear
def get_scraped():
    # la url destino
    global url
    url = 'https://ycharts.com/companies/TSLA/revenues'

    # Rotacion User-Agent para evitar bloqueos
    user_agent_list = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
    ]
    for i in range(1, 4):
        user_agent = random.choice(user_agent_list)

    headers = {'User-Agent': user_agent}
    
    # llevar acabo la request y comprobar que fue exitosa
    response = requests.get(url, headers=headers)
    time.sleep(9)
    if response.status_code == 200:
        html_data = response.text
        global soup
        soup = BeautifulSoup(response.content, 'html.parser')

    else:
        print(f"There was an error with code: {response.status_code}")

# llamamos la funcion para recuperar los datos
get_scraped()
# creo listas vacías para almacenar mis valores
v_list = []
d_list = []

# usando las funciones find_all, encuentro la informacion que quiero del html
tables = soup.find_all('table', class_='table')
dates = tables[0].find_all('td', class_=None) + tables[1].find_all('td', class_=None)
values = tables[0].find_all('td', class_='text-right') + tables[1].find_all('td', class_='text-right')

# guardo la informacion encontrada en mis listas
for value in values:
    v_list.append(value.text.strip())
for date in dates:
    d_list.append(date.text.strip())

# Creando el DataFrame a partir de mis listas
dicto = {'Date': d_list, 'Value': v_list}
df = pd.DataFrame(dicto)

#Procesando y limpiando el DataFrame
df['Date'] = pd.to_datetime(df['Date'])
in_b = {'M': '*0.001', 'B': ''}
df['Value'] = df['Value'].replace(in_b, regex=True).map(pd.eval).round(3)


# Ahora a guardarlo en una base de datos

# cargar el archivo .env
load_dotenv()

# Conectar con la base de datos
def connect():
    global engine 
    connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?"
    print("Starting the connection...")
    engine = create_engine(connection_string)
    engine.connect()
    return engine



# Insertar la Tabla en la base de datos
df.to_sql('Tesla_historic_value', con=connect(), if_exists='replace', index=False)


# Cerrar la sesión
with engine.connect() as conn:
    conn.commit()
    conn.close()


# Ahora visualizaremos los datos
plt.plot(df['Date'], df['Value'])
plt.xticks()
plt.show()


