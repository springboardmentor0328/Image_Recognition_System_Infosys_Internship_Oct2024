from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model # type: ignore
from tensorflow.keras.applications import MobileNetV2 # type: ignore
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained MobileNetV2 model for embeddings
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg', input_shape=(224, 224, 3))
model = Model(inputs=base_model.input, outputs=base_model.output)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

# Load known embeddings and labels from the Excel file
def load_embeddings_from_excel(excel_file):
    df = pd.read_excel(excel_file)
    labels = df['Label'].tolist()
    embeddings = df.iloc[:, 2:].values  # Embeddings start from the 3rd column
    return labels, embeddings

known_labels, known_embeddings = load_embeddings_from_excel('embeddings.xlsx')

# Global variables
camera = cv2.VideoCapture(0)

# Function to generate video frames
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Grayscale conversion for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Extract face ROI
            face_roi = frame[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (224, 224))
            face_roi = face_roi.astype('float32') / 255.0
            face_roi = np.expand_dims(face_roi, axis=0)

            # Get embedding and find match
            embedding = model.predict(face_roi, verbose=0)[0]
            if len(known_embeddings) > 0:
                similarities = cosine_similarity([embedding], known_embeddings)[0]
                best_match_index = np.argmax(similarities)
                confidence = similarities[best_match_index]

                # Display the label if similarity exceeds threshold
                if confidence > 0.6:  # Adjust threshold as needed
                    label = known_labels[best_match_index]
                    cv2.putText(frame, f"{label} ({confidence:.2f})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (255, 255, 255), 2)

        # Encode the frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to accept new images for training
@app.route('/train', methods=['POST'])
def train():
    uploaded_files = request.files.getlist("images")
    person_name = request.form['name']
    save_path = os.path.join('dataset', person_name)
    os.makedirs(save_path, exist_ok=True)

    # Save images
    for file in uploaded_files:
        file.save(os.path.join(save_path, file.filename))

    # Re-train embeddings
    load_dataset_to_excel('dataset', 'embeddings.xlsx') # type: ignore
    global known_labels, known_embeddings
    known_labels, known_embeddings = load_embeddings_from_excel('embeddings.xlsx')

    return jsonify({"message": "Training successful"}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
