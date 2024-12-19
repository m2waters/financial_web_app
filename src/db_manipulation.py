import sqlite3

connection = sqlite3.connect('database.db')


def refresh_db():

    with open('schema.sql') as f:
        connection.executescript(f.read())

def view_db():

    cur = connection.cursor()
    table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' ")]
    print(table_list)
    for row in cur.execute("SELECT * FROM reddit_posts"):
        print(row)

print("Hi\n")
print("What would you like to do today?\n\n")
print("1) Refresh and clear database creating new tables\n")
print("2) View database contents\n")
print("3) Cancel and close program")

x = 0
while x == 0:
    resp = input()
    if resp == "1":
        refresh_db()
        x = 1
    elif resp == "2":
        view_db()
        x = 1
    elif resp == "3":
        x = 1
    else:
        print("Please choose one of the available options by entering 1, 2 or 3 and pressing enter")