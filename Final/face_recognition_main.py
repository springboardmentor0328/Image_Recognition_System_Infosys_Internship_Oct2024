import face_recognition
import pickle
import cv2
import numpy as np

# Load face encodings and names from the pickle file
try:
    with open('face_encodings.pkl', 'rb') as f:
        encodings_data = pickle.load(f)  # Load as dictionary
        known_face_encodings = list(encodings_data.values())
        known_face_names = list(encodings_data.keys())
except FileNotFoundError:
    print("Encoding file not found. Please make sure 'face_encodings.pkl' exists.")
    exit()

# Initialize video capture from webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open video capture.")
    exit()

print("Press 'q' to exit the face recognition.")

while True:
    # Capture frame from webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image. Exiting.")
        break

    # Resize frame for faster processing (1/4 size)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and compute face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop over each detected face and attempt recognition
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if face_distances[best_match_index] < 0.6:  # Threshold for confidence
            name = known_face_names[best_match_index]
            confidence = (1 - face_distances[best_match_index]) * 100
            label = f"{name} ({confidence:.2f}%)"
            color = (0, 255, 0)  # Green for recognized faces
        else:
            label = "Unknown"
            color = (0, 0, 255)  # Red for unrecognized faces

        # Scale face locations back to the original frame size
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

        # Draw a rectangle around the face and display the label
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()

