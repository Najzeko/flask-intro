import sqlite3
import csv

connection = sqlite3.connect("LumberFut.db")
cursor = connection.cursor()

with open("LumberFut.csv", "r") as file:
    num_records = 0
    next(file)      #skip first line with column names
    for row in file:
        print(row.split(","))
        cursor.execute("INSERT OR REPLACE INTO FuturesTable VALUES (?, ?, ?, ?, ?, ?, ?)", row.split(","))
        connection.commit()
        num_records += 1
connection.close()
print("records transferred: ", num_records)