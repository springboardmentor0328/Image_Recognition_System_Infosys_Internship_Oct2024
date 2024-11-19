from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import cv2
import os
from face_recognize import FaceRecognizer

app = Flask(__name__)
recognizer = FaceRecognizer()

# Directory for storing user datasets
DATASET_DIR = "datasets"
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/recognition')
def recognition():
    return render_template('recognition.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"status": "error", "message": "Username is required"}), 400

    # Check if the username already exists
    user_path = os.path.join(DATASET_DIR, username)
    if os.path.exists(user_path):
        # Redirect to the home page if the user exists
        return jsonify({"status": "error", "redirect": url_for('home'), "message": "User already exists."}), 200

    # Create the user directory if it does not exist
    os.makedirs(user_path)
    return jsonify({"status": "success", "message": "Starting face registration..."})

@app.route('/register_stream', methods=['GET'])
def register_stream():
    username = request.args.get('username')
    if not username:
        return Response("data: Error - Username is required\n\n", mimetype="text/event-stream")

    return Response(recognizer.register_user_stream(username), mimetype="text/event-stream")


def generate_frames():
    webcam = cv2.VideoCapture(0)
    while True:
        success, frame = webcam.read()
        if not success:
            break
        else:
            # Perform face recognition
            frame = recognizer.recognize_faces(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
