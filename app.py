from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connections():
    conn = sqlite3.connect('database.db')
    return conn

def convert_tuple_to_list(tup):
    array = []
    for i in tup:
        new_list = list(i)
        array.append(new_list)
    return array

@app.route("/")
def index():
    conn = get_db_connections()
    data = conn.execute('SELECT * FROM financials').fetchall()
    data = convert_tuple_to_list(data)
    return render_template('index.html',
                           data=data)