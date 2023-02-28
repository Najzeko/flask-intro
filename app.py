from flask import Flask, render_template
import sqlite3
import pandas as pd
import json
import plotly
import numpy as np

pd.options.plotting.backend = "plotly"
app = Flask(__name__)
connection = sqlite3.connect("LumberFut.db", check_same_thread=False)
type_dict = {
    "Open": np.float64,
    "High": np.float64,
    "Low": np.float64,
    "Close*": np.float64,
    "Adj Close**": np.float64,
    "Volume": np.float64    
    }

@app.route('/')
def root():
    data = pd.read_sql_query("SELECT * FROM FuturesTable", connection, parse_dates=['Date'])#, dtype=type_dict)
    data = data.apply(pd.to_numeric, errors='coerce')
    data.dropna(inplace=True)
    graph_data = data["Open"]
    print(data)
    print(data.dtypes)
    print(graph_data)
    fig = graph_data.plot.line()
    #fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html', graphJSON=graphJSON)