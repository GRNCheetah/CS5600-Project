import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO submissions (id, answers) VALUES (?, ?)",
            ('1', 'blah blah content')
            )

cur.execute("INSERT INTO submissions (id, answers) VALUES (?, ?)",
            ('3', '[\'J2\', \'P0\']')
            )

connection.commit()
connection.close()