import pyodbc
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import logging
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=newsscrapperserver.database.windows.net;'
                        'Database=news-scrapper-db;'
                        'UID=adminIgor;'
                        'PWD=Kaffee-1')
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute('DELETE FROM news')
    date_time = datetime.datetime.now().strftime("%Y-%m-%d")

    sites= dict({'spiegel': ['https://www.spiegel.de/thema/ukraine_konflikt/','span','hover:opacity-moderate focus:opacity-moderate'], 
                'tagesschau': ['https://www.tagesschau.de/thema/ukraine/','span','teaser__headline'], 
                'focus.ua': ['https://focus.ua/voennye-novosti','div','c-card__title'], 
                'tsn': ['https://tsn.ua/','a','c-card__link']
                })

    for key in sites:

        # Web scraper
        url = sites[key][0]
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'lxml')
        stats = soup.find_all(sites[key][1], class_ = sites[key][2])
        stats = list(stat.text.replace("'","").strip() for stat in stats)
        stats = list(dict.fromkeys(stats))[:10]

        for stat in stats:
            cursor.execute(f"INSERT INTO news (NAME, DATE, LINK) VALUES {key,date_time,stat}")

        conn.commit()

    conn.close()    




