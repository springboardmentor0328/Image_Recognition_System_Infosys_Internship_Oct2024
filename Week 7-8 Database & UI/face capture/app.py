from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
import time
import sqlite3
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model

app = Flask(__name__)

# Initialize OpenCV variables
camera = cv2.VideoCapture(0)  # Change 0 to your camera index if needed
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
position_count = [0, 0, 0]  # Counts for center, left, right
current_instruction = 0
username = None
save_dir_base = "captured_faces"
db_file = "embeddings.db"
capture_complete = False  # To indicate the capture process is done


def ensure_user_dir():
    """Ensure user-specific directory exists."""
    global save_dir_base, username
    save_dir = os.path.join(save_dir_base, username)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def capture_frames():
    global current_instruction, position_count, username, capture_complete
    if username is None:
        return

    save_dir = ensure_user_dir()

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Create a copy of the frame without the green rectangle for saving
        save_frame = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        # Define rectangle region for alignment
        height, width = frame.shape[:2]
        rect_x1, rect_y1 = width // 4, height // 4
        rect_x2, rect_y2 = 3 * width // 4, 3 * height // 4
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 2)

        # Instruction text
        if current_instruction < len(instructions):
            cv2.putText(frame, instructions[current_instruction], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        face_detected_in_region = False
        for (x, y, w, h) in faces:
            # Check if face is within the rectangle region
            if rect_x1 < x + w // 2 < rect_x2 and rect_y1 < y + h // 2 < rect_y2:
                face_detected_in_region = True
                # Save face if not already captured
                if position_count[current_instruction] < 15:
                    face_img = save_frame[y:y + h, x:x + w]
                    save_path = os.path.join(save_dir, f"pos{current_instruction}_{position_count[current_instruction]}.jpg")
                    cv2.imwrite(save_path, face_img)
                    position_count[current_instruction] += 1
                    time.sleep(0.5)

                    # Check if 15 images are captured for the current position
                    if position_count[current_instruction] == 15:
                        current_instruction += 1
                        if current_instruction >= len(instructions):
                            capture_complete = True
                            return  # Stop video feed after capturing
                        else:
                            # Show position change instruction
                            cv2.putText(frame, "Changing Position...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                            time.sleep(1)
                        break

        # Feedback if no face is detected
        if not face_detected_in_region and current_instruction < len(instructions):
            cv2.putText(frame, "Face not detected in the center region", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Encode frame as JPEG for web streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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

        # Resize and normalize image
        img = cv2.resize(img, (224, 224))
        img = img.astype('float32') / 255.0
        img = np.expand_dims(img, axis=0)

        # Extract embedding
        embedding = model.predict(img)[0]
        embedding_str = ','.join(map(str, embedding))

        # Insert into database
        cursor.execute("INSERT INTO embeddings (label, embedding) VALUES (?, ?)", (username, embedding_str))

    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    global username, position_count, current_instruction, capture_complete
    if request.method == 'POST':
        username = request.form['username']
        position_count = [0, 0, 0]  # Reset counts for a new user
        current_instruction = 0
        capture_complete = False
        return redirect(url_for('capture'))

    return render_template('index.html')


@app.route('/capture', methods=['GET', 'POST'])
def capture():
    global capture_complete, username
    if request.method == 'POST':
        # Save embeddings to SQLite after capture
        save_to_sql(os.path.join(save_dir_base, username))
        return redirect(url_for('done'))
    return render_template('capture.html')


@app.route('/done')
def done():
    return render_template('done.html')


@app.route('/video_feed')
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    os.makedirs(save_dir_base, exist_ok=True)  # Ensure base directory exists
    app.run(debug=True)
