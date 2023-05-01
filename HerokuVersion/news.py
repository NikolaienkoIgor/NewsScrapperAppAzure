
import pandas as pd
import psycopg2
import requests
from bs4 import BeautifulSoup
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# DB connect
db_name = "d5m8kvgvikj9bk"
db_user = "rtgqqcatiifypo"
db_password = "d5d99c00ff5a8aadf2cc9a61e4f1486252f8fb178f3556ea72badb224e18f66d"
db_host = "ec2-54-220-14-54.eu-west-1.compute.amazonaws.com"
db_port = 5432

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port = db_port)
cursor = conn.cursor()
conn.autocommit = True

# DB create
# cursor.execute('''CREATE TABLE news (
#                                         ID         serial PRIMARY KEY,
#                                         NAME       varchar(5000) NOT NULL,
#                                         DATE       date,
#                                         LINK       varchar(5000) NOT NULL
#                                      )''')

cursor.execute('DELETE FROM news')

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
    
    # Insert
    date_time = datetime.datetime.now().strftime("%Y-%m-%d")
    for stat in stats:
        cursor.execute(f"INSERT INTO news (name,date,link) VALUES {key,date_time,stat}")

# Select
cursor.execute('SELECT * FROM news')
df = pd.DataFrame.from_records(cursor.fetchall(),
                               columns = [desc[0] for desc in cursor.description])

conn.close()

msg = MIMEMultipart()
msg['From'] = "radim.duboff@outlook.com"
msg['To'] = "nikolaienko@hotmail.de"
msg['Subject'] = "News"

html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(df.to_html())

part1 = MIMEText(html, 'html')
msg.attach(part1)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
s.starttls() #Puts connection to SMTP server in TLS mode
s.ehlo()
s.login('nikolaienkoigor@googlemail.com', 'fjqfajrotzwafnvf')

s.sendmail(msg['From'], msg['To'], msg.as_string())

s.quit()

print('process completed')

