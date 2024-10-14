import requests
import pandas as pd
import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

def convert_unix_to_datetime(unix):
    return datetime.fromtimestamp(unix/1000)

def increase_in_value(value):
    if value > 0:
        return 1
    elif value <= 0:
        return 0

r = requests.get('https://api.polygon.io/v2/aggs/ticker/AAPL/range/15/minute/2023-02-27/2024-02-27?adjusted=true&sort=asc&limit=50000&apiKey=KYr7DZiVgvC7FpOSt4G7aovObo1Q3qs2')
# print(r.text[0])
j = json.loads(r.text)
# print(j)
# df = pd.read_json('https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-02-27/2024-02-27?adjusted=true&sort=asc&limit=50000&apiKey=KYr7DZiVgvC7FpOSt4G7aovObo1Q3qs2')

results = pd.DataFrame(j['results'])
results.rename(columns={'v': 'volume', 'vw': 'volume_weighted', 'o': 'opening_value', 'c': 'closing_value', 'h': 'high', 'l': 'low', 't': 'datetime', 'n': 'trades'}, inplace=True)
print(results.head())


results['datetime'] = results['datetime'].apply(convert_unix_to_datetime)
results['open_close_difference'] = results['closing_value'] - results['opening_value']
results['increase_in_value'] = results['open_close_difference'].apply(increase_in_value)

print(results.head())

plt.plot(results['datetime'], (results['high']))
plt.plot(results['datetime'], (results['low']))
plt.plot(results['datetime'], (results['volume_weighted']))
plt.show()
