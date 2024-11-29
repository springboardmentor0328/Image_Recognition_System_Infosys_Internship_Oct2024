import streamlit as st
import cv2
import numpy as np
import os
import time

# Haar Cascade file for face detection
haar_file = 'haarcascade_frontalface_default.xml'

# Directory for storing datasets
datasets = 'datasets'
if not os.path.isdir(datasets):
    os.mkdir(datasets)

# Image size
(width, height) = (130, 100)

# Initialize Streamlit session state variables
if "registering" not in st.session_state:
    st.session_state.registering = False

if "recognizing" not in st.session_state:
    st.session_state.recognizing = False

if "stop_recognition" not in st.session_state:
    st.session_state.stop_recognition = False

# Streamlit app title
st.title("Face Recognition System")

# Function to capture dataset images
def capture_images(name):
    path = os.path.join(datasets, name)
    if not os.path.isdir(path):
        os.mkdir(path)

    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)

    directions = ["front", "left", "right", "up"]  # Order of prompts
    stframe = st.empty()  # Placeholder for the video frame

    # Capture images for each direction
    for direction in directions:
        # Show instruction to look in the specified direction
        st.write(f"Please look {direction.capitalize()}...")
        instruction_start_time = time.time()

        while time.time() - instruction_start_time < 2:
            # Display live video feed with yellow instruction
            ret, frame = webcam.read()
            if not ret:
                st.error("Webcam not detected. Please check your camera settings.")
                return

            cv2.putText(frame, f"Look {direction.capitalize()}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # Yellow text
            stframe.image(frame, channels="BGR", caption="Preparing to Capture", use_container_width=True)

        # Begin capturing images for the current direction
        count = 0
        while count < 25:
            ret, frame = webcam.read()
            if not ret:
                st.error("Webcam not detected. Please check your camera settings.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite(f'{path}/{direction}_{count + 1}.png', face_resize)
                count += 1

                # Draw rectangle and display notification
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Capturing {direction.capitalize()} ({count}/25)", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            stframe.image(frame, channels="BGR", caption="Capturing Images", use_container_width=True)

    webcam.release()
    st.success(f"Captured images for {name} in all directions.")

# Function to recognize faces
def recognize_faces():
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)

    # Train the model
    (images, labels, names, id) = ([], [], {}, 0)
    for subdir in os.listdir(datasets):
        names[id] = subdir
        for filename in os.listdir(os.path.join(datasets, subdir)):
            path = os.path.join(datasets, subdir, filename)
            images.append(cv2.imread(path, 0))
            labels.append(id)
        id += 1

    if len(images) == 0:
        st.error("No face data found. Please register faces first.")
        return

    (images, labels) = [np.array(lst) for lst in [images, labels]]
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, labels)

    st.write("Recognizing faces. Press 'Stop Recognition' to end.")
    stframe = st.empty()  # Placeholder for the video frame

    while not st.session_state.stop_recognition:
        ret, frame = webcam.read()
        if not ret:
            st.error("Webcam not detected. Please check your camera settings.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))

            prediction = model.predict(face_resize)
            confidence = prediction[1]

            if confidence < 100:
                name = names[prediction[0]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} - {confidence:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        stframe.image(frame, channels="BGR", caption="Recognition in Progress", use_container_width=True)

    webcam.release()
    st.success("Recognition stopped.")

# Main Interface
col1, col2 = st.columns(2)

# Register New Face
with col1:
    if st.button("Register New Face"):
        st.session_state.registering = True
        st.session_state.recognizing = False
        st.session_state.stop_recognition = False

    if st.session_state.registering:
        st.subheader("Register New Face")
        name = st.text_input("Enter the name for the new face:")
        if st.button("Start Registration"):
            if name:
                capture_images(name)
                st.session_state.registering = False  # Reset state
            else:
                st.error("Please enter a name before starting.")

# Recognize Faces
with col2:
    if st.button("Recognize Faces"):
        st.session_state.recognizing = True
        st.session_state.registering = False
        st.session_state.stop_recognition = False

    if st.session_state.recognizing:
        st.subheader("Face Recognition")
        start_recognition = st.button("Start Recognition")
        stop_recognition = st.button("Stop Recognition")

        if start_recognition:
            st.session_state.stop_recognition = False
            recognize_faces()

        if stop_recognition:
            st.session_state.stop_recognition = True
