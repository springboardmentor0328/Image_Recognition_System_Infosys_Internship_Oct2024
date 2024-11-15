import sqlite3

def row_deletion(name):
    """Delete rows with the given name from the SQLite database."""
    # Connect to the SQLite database
    connection = sqlite3.connect('face_recognition.db')
    cursor = connection.cursor()

    # Execute the DELETE query
    cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
    connection.commit()

    # Get the number of rows deleted
    deleted_rows = cursor.rowcount
    print(f"{deleted_rows} rows deleted.")
    connection.close()

