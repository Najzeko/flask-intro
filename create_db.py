import sqlite3

connection = sqlite3.connect("LumberFut.db")
cursor = connection.cursor()

query = """
    CREATE TABLE FuturesTable (
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        adj_close REAL,
        volume INTEGER,
        primary key(date)
        ) """
cursor.execute(query)
connection.commit()
connection.close()