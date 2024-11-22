import cv2
import os
import numpy as np
import sqlite3

# Path to the SQLite database
db_path = 'face_recognition.db'
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

label_dict = {}

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect(db_path)

# Load images and labels from the database
def load_images_and_labels_from_db():
    images = []
    labels = []
    current_label = 0

    # Connect to the database
    conn = connect_db()
    c = conn.cursor()

    # Fetch all the faces and their labels from the database
    c.execute("SELECT id, name, image FROM faces")
    rows = c.fetchall()

    for row in rows:
        label = current_label
        person_name = row[1]
        img_data = row[2]

        # Store the label in the dictionary
        label_dict[label] = person_name

        # Convert the binary image data to a numpy array
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(img, 1.1, 5)
        for (x, y, w, h) in faces:
            face = cv2.resize(img[y:y+h, x:x+w], (200, 200))
            images.append(face)
            labels.append(label)

        current_label += 1

    conn.close()
    return images, np.array(labels, dtype=np.int32)

# Function to train the recognizer with the loaded images and labels
images, labels = load_images_and_labels_from_db()
if len(images) > 0 and labels.size > 0:
    recognizer.train(images, labels)  # Train the model
    print("Model training complete.")
else:
    print("No data to train on. Check the database for stored images.") 

# Real-time face recognition using webcam
def recognize_faces():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    frame_skip = 2  # Process every 2nd frame to reduce lag
    frame_count = 0
    unknown_threshold = 50  # Set threshold for recognizing unknown faces

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera")
            break  # Stop if frame reading fails

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip this frame to reduce lag

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.04, minNeighbors=7, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Resize the detected face for recognition
            face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label, confidence = recognizer.predict(face)

            # Check confidence to determine if face is recognized or "Unknown"
            if confidence < unknown_threshold:
                label_text = label_dict.get(label, "Unknown")
                text = f"{label_text} ({100 - confidence:.2f}%)"
                color = (0, 255, 0)  # Green for recognized face
            else:
                text = f"unknown ({100 - confidence:.2f}%)"
                color = (0, 0, 255)  # Red for unknown face

            # Draw bounding box and text
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Face Recognition', frame)

        # Press 'Esc' to exit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Train the model if data exists
    images, labels = load_images_and_labels_from_db()
    if len(images) > 0 and labels.size > 0:
        train_model()  # Train the model
        recognize_faces()  # Start real-time face recognition
    else:
        print("Face recognizer is not trained due to insufficient or missing training data.")
