import pandas as pd
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    
    sites= dict({'spiegel': ['https://www.spiegel.de/thema/ukraine_konflikt/','span','hover:opacity-moderate focus:opacity-moderate'], 
                'tagesschau': ['https://www.tagesschau.de/thema/ukraine/','span','teaser__headline'], 
                'focus.ua': ['https://focus.ua/voennye-novosti','div','c-card__title'], 
                'tsn': ['https://tsn.ua/','a','c-card__link']
                })

    df = pd.DataFrame(columns=['Titles', 'Website']) 

    for key in sites:

        # Web scraper
        url = sites[key][0]
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'lxml')
        stats = soup.find_all(sites[key][1], class_ = sites[key][2])
        stats = list(stat.text.replace("'","").strip() for stat in stats)
        stats = list(dict.fromkeys(stats))[:10]

        for stat in stats:
            df = df.append({'Titles': stat, 'Website': key}, ignore_index=True)

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

    print('completed')    
