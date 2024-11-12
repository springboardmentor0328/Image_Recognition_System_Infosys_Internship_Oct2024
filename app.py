from flask import Flask, render_template, request, jsonify
import capture  # Import capture functions from capture.py
import inference

app = Flask(__name__)

# Route to render the home page with the input form
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the face capture
@app.route('/start_capture', methods=['POST'])
def start_capture():
    data = request.get_json()
    person_name = data.get('name')  # Get the name from JSON payload
    if person_name:  # Proceed only if a name is provided
        capture.capture_images(person_name)  # Call the capture function with the name
        return jsonify(status=f"Started capturing for {person_name}")
    else:
        return jsonify(status="Error: No name provided"), 400

# Function to start face recognition in a separate thread
def run_recognition():
    capture.recognize_faces()  # Call the actual recognition function

# Route to start face recognition
@app.route('/start_recognition', methods=['GET'])
def start_recognition():
    try:
        # Call your recognition function or process here
        recognition_status = inference.recognize_faces()  # Placeholder for your recognition logic

        return jsonify({"status": recognition_status})

    except Exception as e:
        print(f"Recognition error: {e}")
        return jsonify({"status": "Recognition failed.", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
