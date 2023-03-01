from flask import Flask, render_template
import sqlite3
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import numpy as np

pd.options.plotting.backend = "plotly"
app = Flask(__name__)
connection = sqlite3.connect("LumberFut.db", check_same_thread=False)
# type_dict = {
#     "Open": np.float64,
#     "High": np.float64,
#     "Low": np.float64,
#     "Close*": np.float64,
#     "Adj Close**": np.float64,
#     "Volume": np.float64    
#     }
datetime_dict = {"yearfirst": True}
colours = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

def get_data(connection, datetime_dict):
    return pd.read_sql_query("SELECT * FROM FuturesTable", connection, parse_dates={'Date': datetime_dict})#['Date'])#, dtype=type_dict)

def clean_data(data):
    cols = data.columns.difference(['Date'])
    data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')
    data.dropna(inplace=True)
    #data.set_index('Date', inplace=True)
    return data

def plot_data(data):
    print(data)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["Open"], 
                   name="Open",
                   visible=False,
                   line=dict(color=colours[0])))
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["High"], 
                   name="High",
                   visible=False,
                   line=dict(color=colours[1])))
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["Low"], 
                   name="Low",
                   visible=False,
                   line=dict(color=colours[2])))
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["Close*"], 
                   name="Close*",
                   line=dict(color=colours[3])))
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["Adj Close**"], 
                   name="Adj Close**",
                   visible=True,
                   line=dict(color=colours[4])))
    fig.add_trace(
        go.Scatter(x=data["Date"],
                   y=data["Volume"], 
                   name="Volume",
                   visible=False,
                   line=dict(color=colours[5])))

    fig.update_layout(
        width=1800,
        height=900,
        autosize=True,
        margin=dict(t=100, b=100, l=100, r=100),
        template="plotly_dark",
    )
    return fig


    

@app.route('/')
def root():
    data = get_data(connection, datetime_dict)
    data = clean_data(data)

    
    
    #graph_data = data[["Open", "High", "Low"]]
    print(data)
    print(data.dtypes)
    #print(graph_data)

    # fig = df.plot(title="Pandas Backend Example", template="simple_white",
    #           labels=dict(index="time", value="money", variable="option"))
    #fig = graph_data.plot(title="Lumber Futures", template="plotly_dark", labels=dict(index="Date", value="Amount in USD", variable="amount"))

    #fig.show()
    fig = plot_data(data)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('notdash.html', graphJSON=graphJSON)