
import cv2
import time
import face_recognition
import numpy as np
import streamlit as st
import sqlite3

# Displaying the rectangle and instructions in the video feed
def display_pose_instructions(frame, instruction, rect_coords):
    """Displays the instruction and the guidance rectangle in the camera feed."""
    # Draw the fixed rectangle for the user to pose inside
    cv2.rectangle(frame, (rect_coords[0], rect_coords[1]), (rect_coords[2], rect_coords[3]), (255, 0, 0), 2)
    
    # Display instruction on the feed
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, instruction, (50, 50), font, 1, (255, 255, 0), 2, cv2.LINE_AA)

# Function to handle user registration (new user posing and capture)
def register_user(name):
    st.title("Register New User")
    
    # Start the video capture and show live feed
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        st.error("Unable to access the camera. Please check your camera settings.")
        return

    frame_placeholder = st.empty()  # Placeholder to update the frame in Streamlit
    
    # Increased rectangle size and fixed position (centered)
    rect_width = 500  # Width of the rectangle (increased size)
    rect_height = 400  # Height of the rectangle (increased size)
    screen_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    screen_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the center coordinates for the rectangle
    center_x = screen_width // 2
    center_y = screen_height // 2
    rect_coords = (
        center_x - rect_width // 2,  # Left X coordinate
        center_y - rect_height // 2,  # Top Y coordinate
        center_x + rect_width // 2,  # Right X coordinate
        center_y + rect_height // 2  # Bottom Y coordinate
    )

    # Instructions for user posing
    instructions = [
        "Please face the camera directly.",
        "Now, look to your right.",
        "Now, look to your left.",
        "Now, look up.",
        "Now, look down."
    ]
    
    # Capture the user's face from different angles
    face_encodings = []
    face_locations = []

    for i, instruction in enumerate(instructions):
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to capture frame.")
            break

        # Show instructions and rectangle on the live camera feed
        display_pose_instructions(frame, instruction, rect_coords)
        
        # Display live camera feed with instructions
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", caption=f"Register User: {name}", use_container_width=True)
        
        # Wait for user to pose
        time.sleep(3)  # Give user time to pose for each instruction (3 seconds)

        # Capture face encodings if a face is detected
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(face_encodings_in_frame) > 0:
            face_encodings.append(face_encodings_in_frame[0])  # Capture the first detected face encoding

    # Check if any faces were captured
    if len(face_encodings) > 0:
        # Save the face encoding into the database
        conn = sqlite3.connect('faces.db')
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute('SELECT name FROM users WHERE name=?', (name,))
        result = cursor.fetchone()
        if result:
            st.warning(f"Name '{name}' already exists. Try another name.")
            return
        else:
            # Insert the new user's face encoding into the database
            cursor.execute('INSERT INTO users (name, encoding) VALUES (?, ?)', 
                           (name, face_encodings[0].tobytes()))
            conn.commit()
            st.success(f"User '{name}' registered successfully!")
            
    else:
        st.warning("No face detected. Please ensure you are posing correctly in front of the camera.")
    
    video_capture.release()


