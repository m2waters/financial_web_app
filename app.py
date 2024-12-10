from flask import Flask, render_template, request, redirect
import sqlite3
import requests
import pandas as pd
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sqlite3
import io
import base64
from dotenv import load_dotenv
import os

###########################################

app = Flask(__name__)

###########################################
########    FUNCTIONS   ###################
###########################################

def get_db_connections():
    conn = sqlite3.connect('database.db')
    return conn



def convert_tuple_to_list(tup):
    array = []
    for i in tup:
        new_list = list(i)
        array.append(new_list)
    return array


def convert_unix_to_datetime(unix):
        return datetime.fromtimestamp(unix/1000)


def increase_in_value(value):
        if value > 0:
            return 1
        elif value <= 0:
            return 0


def fig_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img,
                    format='png',
                    bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())

def plot(x_data_list, y_data_list):
     
    fig, ax = plt.subplots()
    fig.set_figwidth(18)
    for i in range(len(x_data_list)):
        ax.plot(x_data_list[i], y_data_list[i])
    return "data:image/png;base64, " + fig_to_base64(fig).decode('utf-8')


def pull_data(ticker='AAPL', start_date='2023-02-27', end_date='2024-02-27'):

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    api = 'https://api.polygon.io/v2/aggs/ticker/' + ticker + '/range/15/minute/' + start_date + '/' + end_date + '?adjusted=true&sort=asc&limit=50000&apiKey=' + API_KEY
    j = json.loads((requests.get(api)).text)

    results = pd.DataFrame(j['results'])
    results.rename(columns={'v': 'volume', 'vw': 'volume_weighted', 'o': 'opening_value', 'c': 'closing_value', 'h': 'high', 'l': 'low', 't': 'datetime', 'n': 'trades'}, inplace=True)
    results['datetime'] = results['datetime'].apply(convert_unix_to_datetime)
    results['open_close_difference'] = results['closing_value'] - results['opening_value']
    results['increase_in_value'] = results['open_close_difference'].apply(increase_in_value)

    x_list = [results['datetime']]    
    y_list = [results['high']]

    link = plot(x_list, y_list)

    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()
    for i in range(len(results)):       
        cur.execute("INSERT INTO financials (created, company, volume, volume_weighted, opening_value, closing_value, high, low, trades) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (str(results['datetime'][i]),
                    ticker,
                    int(results['volume'][i]),
                    float(results['volume_weighted'][i]),
                    float(results['opening_value'][i]),
                    float(results['closing_value'][i]),
                    float(results['high'][i]),
                    float(results['low'][i]),
                    int(results['trades'][i]),
                    )                
                )
    cur.execute("INSERT INTO figures (title, link) VALUES (?, ?)",
                ("TestPlot",
                link
                )
            )
    
    plt.close()

    connection.commit()
    connection.close()

#####################################################
############    ROUTES   ############################
#####################################################

@app.route("/")
def index():
    conn = get_db_connections()
    data = conn.execute('SELECT * FROM financials').fetchall()
    figs = conn.execute('SELECT * FROM figures').fetchall()
    data = convert_tuple_to_list(data)
    return render_template('index.html',
                           data=data,
                           figs=figs)

@app.route('/data')
def data():
    conn = get_db_connections()
    data = conn.execute('SELECT * FROM financials').fetchall()
    figs = conn.execute('SELECT * FROM figures').fetchall()
    data = convert_tuple_to_list(data)
    return render_template('data.html',
                           data=data,
                           figs=figs)


@app.route('/update-data', methods=['POST'])
def update_data():
    ticker = request.form['ticker']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    print(ticker, start_date, end_date)
    print(type(ticker), type(start_date), type(end_date))

    pull_data(ticker, start_date, end_date)

    return redirect(request.referrer)
