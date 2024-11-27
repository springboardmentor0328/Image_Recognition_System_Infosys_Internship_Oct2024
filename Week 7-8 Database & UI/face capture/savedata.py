import sqlite3

# Path to the database file
db_file = "embeddings.db"

def print_unique_usernames(db_file):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to fetch distinct usernames (labels)
    cursor.execute("SELECT DISTINCT label FROM embeddings")
    unique_usernames = cursor.fetchall()

    # Print the unique usernames
    print("Unique Usernames:")
    for username in unique_usernames:
        print(username[0])

    # Close the connection
    conn.close()

# Call the function
print_unique_usernames(db_file)
