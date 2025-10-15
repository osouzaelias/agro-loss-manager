import sqlite3

DATABASE_FILE = 'colheita.db'


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open('infra/database/schema.sql', 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()