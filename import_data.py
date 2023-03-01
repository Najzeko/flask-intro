import sqlite3
import pandas as pd

connection = sqlite3.connect("LumberFut.db")
cursor = connection.cursor()

data = pd.read_excel("data/LumberFut.xlsx", engine='openpyxl')
data.to_sql("FuturesTable", connection, if_exists='replace')
connection.close()
