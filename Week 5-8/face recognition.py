import cv2
import numpy as np
import tensorflow as tf
from mtcnn import MTCNN
from facenet_pytorch import InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
import streamlit as st

# File to store user data
ENCODINGS_FILE = "face_encodings.json"

# Initialize MTCNN and FaceNet models
detector = MTCNN()
facenet = InceptionResnetV1(pretrained='vggface2').eval()

# Load or initialize face encodings database
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "r") as file:
        user_data = json.load(file)
else:
    user_data = {}


# Save encodings to the file
def save_encodings(data):
    with open(ENCODINGS_FILE, "w") as file:
        json.dump(data, file)


# Detect faces and preprocess them
def detect_faces(image):
    detections = detector.detect_faces(image)
    faces = []
    boxes = []
    for det in detections:
        x, y, w, h = det['box']
        face = image[y:y + h, x:x + w]
        face = cv2.resize(face, (160, 160))
        faces.append(face)
        boxes.append((x, y, w, h))
    return faces, boxes


# Get embeddings for faces
def get_embeddings(faces):
    embeddings = []
    for face in faces:
        face = np.expand_dims(face, axis=0) / 255.0  # Normalize pixel values
        embedding = facenet(torch.tensor(face).permute(0, 3, 1, 2).float()).detach().numpy()
        embeddings.append(embedding[0])
    return embeddings


# Streamlit GUI
st.title("Live Face Recognition")
st.sidebar.title("Options")

# Mode Selection
mode = st.sidebar.selectbox("Choose Mode", ["Register New Face", "Verify Live", "Stop Verification"])


# Start Webcam
@st.cache_resource
def start_webcam():
    return cv2.VideoCapture(0)


cap = start_webcam()

if mode == "Register New Face":
    st.header("Register New Face")
    name = st.text_input("Enter Name for Registration")
    if st.button("Register"):
        ret, frame = cap.read()
        if not ret:
            st.error("Unable to access the camera!")
        else:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces, _ = detect_faces(frame_rgb)
            if len(faces) == 0:
                st.error("No face detected! Try again.")
            else:
                embeddings = get_embeddings(faces)
                user_data[name] = embeddings[0].tolist()
                save_encodings(user_data)
                st.success(f"User '{name}' registered successfully!")

elif mode == "Verify Live":
    st.header("Live Face Verification")
    start_verification = st.button("Start Verification")
    stop_verification = st.button("Stop Verification")
    if start_verification:
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to access the camera!")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces, boxes = detect_faces(frame_rgb)
            if len(faces) == 0:
                st.write("No face detected.")
            else:
                embeddings = get_embeddings(faces)
                for i, embedding in enumerate(embeddings):
                    best_match = None
                    highest_similarity = 0
                    for name, stored_embedding in user_data.items():
                        similarity = cosine_similarity([embedding], [np.array(stored_embedding)])[0][0]
                        if similarity > highest_similarity:
                            highest_similarity = similarity
                            best_match = name
                    x, y, w, h = boxes[i]
                    color = (0, 255, 0) if highest_similarity > 0.8 else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{best_match} ({highest_similarity * 100:.2f}%)", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
            if stop_verification:
                break

elif mode == "Stop Verification":
    st.header("Verification Stopped")
    st.write("Switch back to another mode to continue.")
    cap.release()
