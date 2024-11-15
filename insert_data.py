import sqlite3
import cv2

# Path to the SQLite database
db_path = 'face_recognition.db'

# Function to insert an image into the database
def insert_face(name, image_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Failed to read the image at {image_path}")
        return

    # Encode the image as a byte array (BLOB)
    _, img_encoded = cv2.imencode('.jpg', img)
    img_data = img_encoded.tobytes()

    # Insert the data into the faces table
    c.execute("INSERT INTO faces (name, image) VALUES (?, ?)", (name, img_data))

    # Commit and close the connection
    conn.commit()
    conn.close()

    print(f"Inserted image for {name} into the database.")

# Example usage
insert_face('Person Name', 'path_to_image.jpg')
