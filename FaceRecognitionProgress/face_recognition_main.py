import face_recognition
import pickle
import cv2
import numpy as np

# Load face encodings and names from the pickle file
with open('face_encodings.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture image. Exiting.")
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    # Detect faces and compute face encodings
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop over each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare detected face encodings with known faces
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        # Check if the closest known face is a match
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] < 0.6:  # Use a threshold for high confidence
            name = known_face_names[best_match_index]
            confidence = (1 - face_distances[best_match_index]) * 100
            label = f"{name} ({confidence:.2f}%)"
            color = (0, 255, 0)  # Green for recognized
        else:
            label = "Unknown"
            color = (0, 0, 255)  # Red for unrecognized

        # Scale back up face locations and draw box
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    # Display the frame
    cv2.imshow("Face Recognition", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
