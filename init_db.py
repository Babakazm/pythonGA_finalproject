import sqlite3

connection = sqlite3.connect('database.sqlite')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )
cur.execute("INSERT INTO finance (registerer, itemNumber, item,quantity,unitPrice,totalPrice) VALUES (?, ?,?,?,?,?)",
                    ('registerer', 'itemNumber', 'item','quantity','unitPrice','totalPrice'))
connection.commit()
connection.close()
