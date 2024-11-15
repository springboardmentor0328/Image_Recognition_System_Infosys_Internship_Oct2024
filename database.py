# database.py

import sqlite3

# Database file path
db_path = 'face_recognition.db'

def create_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create a table for storing images and their respective names
    c.execute('''CREATE TABLE IF NOT EXISTS faces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    image BLOB NOT NULL
                 )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Database and table created successfully.")
