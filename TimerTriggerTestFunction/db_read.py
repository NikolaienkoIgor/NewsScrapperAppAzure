import pyodbc
import pandas as pd

    
conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                    'Server=newsscrapperserver.database.windows.net;'
                    'Database=news-scrapper-db;'
                    'UID=adminIgor;'
                    'PWD=Kaffee-1')
cursor = conn.cursor()
conn.autocommit = True

cursor.execute('SELECT * FROM news')
df = pd.DataFrame.from_records(cursor.fetchall(),
                               columns = [desc[0] for desc in cursor.description])
print(df)
conn.close()   