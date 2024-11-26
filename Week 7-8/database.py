# database.py
import sqlite3

def create_db():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        encoding BLOB
    )''')
    conn.commit()
    conn.close()

# Call this function to create the database when the project starts
create_db()
