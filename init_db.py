import sqlite3
from server import db

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()

# Create user table in users.db
db.create_all()
