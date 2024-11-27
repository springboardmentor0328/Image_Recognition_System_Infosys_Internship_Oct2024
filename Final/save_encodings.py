import cx_Oracle
import face_recognition
import pickle
import io

# Oracle Database connection setup
dsn_tns = cx_Oracle.makedsn('hostname', 'port', sid='sid')  # Update as needed
connection = cx_Oracle.connect(user='user', password='password', dsn=dsn_tns)

def fetch_images_from_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, image_data FROM user_images")
        rows = cursor.fetchall()
    return rows

def save_encodings():
    encodings_dict = {}

    for username, image_data in fetch_images_from_db():
        # Read the BLOB image data as bytes
        img_data = image_data.read()
        
        # Load the image directly from the byte data using a BytesIO stream
        image = face_recognition.load_image_file(io.BytesIO(img_data))
        
        # Generate encodings
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            encodings_dict[username] = face_encodings[0]  # Save only the first encoding per image

    # Save encodings to a .pkl file
    with open('face_encodings.pkl', 'wb') as f:
        pickle.dump(encodings_dict, f)

    print("Encodings have been saved.")

if __name__ == '__main__':
    save_encodings()
