import cv2
import face_recognition
import sqlite3
import streamlit as st
import numpy as np

# Ensure the 'users' table exists
def create_table_if_not_exists():
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def recognize_faces():
    # Ensure the 'users' table exists
    create_table_if_not_exists()

    video_capture = cv2.VideoCapture(0)
    st.title("Face Recognition")

    # Load stored encodings and names
    conn = sqlite3.connect('faces.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, encoding FROM users')
    known_face_encodings = []
    known_face_names = []
    for row in cursor.fetchall():
        known_face_names.append(row[0])
        known_face_encodings.append(np.frombuffer(row[1], dtype=np.float64))

    frame_placeholder = st.empty()  # Placeholder to update the frame in Streamlit

    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to capture frame.")
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings) > 0:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                # Only proceed if a match is found
                if True in matches:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    name = known_face_names[best_match_index]
                    accuracy = 100 - face_distances[best_match_index]
                    # Use green bounding box for recognized face
                    box_color = (0, 255, 0)  # Green
                else:
                    accuracy = 0.0
                    # Use red bounding box for unknown face
                    box_color = (0, 0, 255)  # Red

                # Draw rectangle around face with the specified color
                cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

                # Display name and accuracy above the bounding box
                text = f"{name} ({accuracy:.2f}%)"
                text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                # cv2.rectangle(frame, (left, top - 25), (left + text_width, top), box_color, -1)  # Background rectangle for text
                cv2.putText(frame, text, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        else:
            # If no face is detected, mark as "Unknown"
            cv2.putText(frame, "No face detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display image in Streamlit (real-time feed)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", caption="Face Recognition", use_container_width=True)

        # Break condition (can be changed if needed, e.g., when pressing 'q')
        if cv2.waitKey(1) & 0xFF == ord('q'):  # If 'q' is pressed, stop recognition
            break

    video_capture.release()
