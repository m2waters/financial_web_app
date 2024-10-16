import requests
import pandas as pd
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import io
import base64


def pull_data(ticker='AAPL'):

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

    r = requests.get('https://api.polygon.io/v2/aggs/ticker/NVDA/range/15/minute/2023-02-27/2024-02-27?adjusted=true&sort=asc&limit=50000&apiKey=KYr7DZiVgvC7FpOSt4G7aovObo1Q3qs2')

    j = json.loads(r.text)


    results = pd.DataFrame(j['results'])
    results.rename(columns={'v': 'volume', 'vw': 'volume_weighted', 'o': 'opening_value', 'c': 'closing_value', 'h': 'high', 'l': 'low', 't': 'datetime', 'n': 'trades'}, inplace=True)

    results['datetime'] = results['datetime'].apply(convert_unix_to_datetime)
    results['open_close_difference'] = results['closing_value'] - results['opening_value']
    results['increase_in_value'] = results['open_close_difference'].apply(increase_in_value)

    print(results.head())


    fig, ax = plt.subplots()

    ax.plot(results['datetime'], (results['high']))
    ax.plot(results['datetime'], (results['low']))

    fig.set_figwidth(18)
    # ax.plot(results['datetime'], (results['volume_weighted']))

    encoded = fig_to_base64(fig)
    link = "data:image/png;base64, " + encoded.decode('utf-8')


    connection = sqlite3.connect('database.db')


    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    for i in range(len(results)):
        
        cur.execute("INSERT INTO financials (created, company, volume, volume_weighted, opening_value, closing_value, high, low, trades) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (str(results['datetime'][i]),
                    "Apple",
                    results['volume'][i],
                    results['volume_weighted'][i],
                    results['opening_value'][i],
                    results['closing_value'][i],
                    results['high'][i],
                    results['low'][i],
                    int(results['trades'][i]),
                    )                
                )

    cur.execute("INSERT INTO figures (title, link) VALUES (?, ?)",
                ("TestPlot",
                link
                )
            )

    connection.commit()
    connection.close()