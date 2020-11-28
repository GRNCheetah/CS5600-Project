import sqlite3

DB_FNAME = 'database.db'
SCHEME_FNAME = 'schema.sql'

def init_tables():
    connection = sqlite3.connect(DB_FNAME)


    with open(SCHEME_FNAME) as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    connection.commit()
    connection.close()

def get_db_connection():
    conn = sqlite3.connect(DB_FNAME)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_tables()