from flask import Flask, render_template, request, jsonify
import threading
import time  # Import the time module
import capture  # Import capture functions from capture.py
import inference  # Import the recognition functions from inference.py
import delete_data as du

app = Flask(__name__)

# Route to render the home page with the input form
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture_page():
    return render_template('capture.html')

@app.route('/delete')
def deletion_page():
    return render_template('user_deletion.html')

# Route to start the face capture
@app.route('/start_capture', methods=['POST'])
def start_capture():
    data = request.get_json()
    person_name = data.get('name')  # Get the name from JSON payload
    if person_name:  # Proceed only if a name is provided
        try:
            capture.capture_images(person_name)  # Call the capture function with the name
            return jsonify(status=f"Started capturing for {person_name}")
        except Exception as e:
            print(f"Capture error: {e}")
            return jsonify(status="Capture failed", error=str(e)), 500
    else:
        return jsonify(status="Error: No name provided"), 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data=request.get_json()
    name = data.get('name')
    name = name.upper()
    if name:
        try:
            du.row_deletion(name) # Call the capture function with the name
            return jsonify(status=f"{name} row deleted successfully")
        except Exception as e:
            print(f"deletion error: {e}")
            return jsonify(status="Deletion failed", error=str(e)), 500
    else:
        return jsonify(status="Error: No name provided"), 400


# Asynchronous recognition function wrapper
def async_recognition():
    try:
        print("Training model...")  # For debugging
        # inference.train_model()  # Train the model before recognition
        print("Recognition started")  # For debugging
        inference.recognize_faces()  # Run recognition from inference.py
    except Exception as e:
        print(f"Recognition error in async_recognition: {e}")


# Route to start face recognition asynchronously
@app.route('/start_recognition', methods=['GET'])
def start_recognition():
    try:
        # Start recognition in a separate thread
        recognition_thread = threading.Thread(target=async_recognition)
        recognition_thread.start()
        print("Recognition thread started")  # For debugging

        # Return initial response
        return jsonify({"status": "Recognition Started"}), 200

    except Exception as e:
        print(f"Recognition error: {e}")
        return jsonify({"status": "Recognition failed.", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=9999)
