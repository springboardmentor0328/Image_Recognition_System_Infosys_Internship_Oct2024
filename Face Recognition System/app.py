from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import os
import time
import sqlite3
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Initialize OpenCV variables
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load MobileNetV2 model for feature extraction
base_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg', input_shape=(224, 224, 3))
model = Model(inputs=base_model.input, outputs=base_model.output)

# Global variables
instructions = [
    "Align your face in the center of the rectangle",
    "Turn your face slightly to the left",
    "Turn your face slightly to the right"
]
position_count = [0, 0, 0]
current_instruction = 0
username = None
save_dir_base = "captured_faces"
db_file = "embeddings.db"
capture_complete = False
c=0

def ensure_user_dir():
    """Ensure user-specific directory exists."""
    global save_dir_base, username
    save_dir = os.path.join(save_dir_base, username)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def save_to_sql(user_dir):
    """Extract embeddings and save them to SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    """)

    for image_name in os.listdir(user_dir):
        image_path = os.path.join(user_dir, image_name)
        img = cv2.imread(image_path)

        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        embedding = model.predict(img)[0]
        embedding_str = ','.join(map(str, embedding))

        cursor.execute("INSERT INTO embeddings (label, embedding) VALUES (?, ?)", (username, embedding_str))

    conn.commit()
    conn.close()


def load_embeddings_from_db():
    """Load embeddings from SQLite database."""
    if not os.path.exists(db_file):
        return 0, 0

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT label, embedding FROM embeddings")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0, 0

    labels = [row[0] for row in rows]
    embeddings = [list(map(float, row[1].split(','))) for row in rows]
    return labels, np.array(embeddings)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index1', methods=['GET', 'POST'])
def index1():
    global username, position_count, current_instruction, capture_complete
    if request.method == 'POST':
        username = request.form['username']
        position_count = [0, 0, 0]
        current_instruction = 0
        capture_complete = False
        return redirect(url_for('capture'))
    return render_template('index1.html')


@app.route('/capture', methods=['GET', 'POST'])
def capture():
    global capture_complete, username
    if request.method == 'POST':
        save_to_sql(os.path.join(save_dir_base, username))
        return redirect(url_for('done'))
    return render_template('capture.html')


@app.route('/done')
def done():
    return render_template('done.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed2')
def video_feed2():
    labels, embeddings = load_embeddings_from_db()
    
    return Response(generate_frames(labels, embeddings), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture_frames():
    global current_instruction, position_count, username, capture_complete, c
    c=0
    if username is None:
        return

    save_dir = ensure_user_dir()

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        save_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        height, width = frame.shape[:2]
        rect_x1, rect_y1 = width // 4, height // 4
        rect_x2, rect_y2 = 3 * width // 4, 3 * height // 4
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)
        if c==43:
            cv2.putText(frame, "Click to Proceed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            if current_instruction < len(instructions):  # Ensure within range
                cv2.putText(frame, instructions[current_instruction], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        face_detected_in_region = False
        for (x, y, w, h) in faces:
            if rect_x1 < x + w // 2 < rect_x2 and rect_y1 < y + h // 2 < rect_y2:
                face_detected_in_region = True
                if position_count[current_instruction] < 15:
                    face_img = save_frame[y:y + h, x:x + w]
                    save_path = os.path.join(save_dir, f"pos{current_instruction}_{position_count[current_instruction]}.jpg")
                    cv2.imwrite(save_path, face_img)
                    position_count[current_instruction] += 1
                    c+=1
                    time.sleep(0.2)
                    
                    if position_count[current_instruction] == 15:
                        current_instruction += 1
                        if current_instruction >= len(instructions):  # Stop capturing
                            capture_complete = True
                            return
                        else:
                            cv2.putText(frame, "Changing Position...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            time.sleep(1)
                        break

                        

        if not face_detected_in_region and current_instruction < len(instructions):
            cv2.putText(frame, "Face not detected in the center region", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if capture_complete:  # Indicate capture is complete
            cv2.putText(frame, "Click on 'Proceed'", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames(labels, embeddings):
    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_roi = frame[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (224, 224))
            face_roi = face_roi.astype('float32') / 255.0
            face_roi = np.expand_dims(face_roi, axis=0)

            embedding = model.predict(face_roi, verbose=0)[0]
            if len(embeddings) > 0:
                similarities = cosine_similarity([embedding], embeddings)[0]
                best_match_index = np.argmax(similarities)
                confidence = similarities[best_match_index]

                if confidence > 0.85:
                    label = labels[best_match_index]
                    cv2.putText(frame, f"{label} ({confidence:.2f})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255), 2)
                

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
    os.makedirs(save_dir_base, exist_ok=True)
    app.run(debug=True)
