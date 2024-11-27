import cv2
import face_recognition
import os

# Initialize lists to hold encodings and names
known_face_encodings = []
known_face_names = []

# Function to load images and encode faces
def load_known_faces(name, image_folder):
    images = os.listdir(image_folder) 
    for image_file in images:
        image_path = os.path.join(image_folder, image_file)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        if encodings:  
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)

# Load multiple images for each person
load_known_faces("Gayathri", r"C:\Users\gayat\FR_project\Gayathri")
load_known_faces("Elon", r"C:\Users\gayat\FR_project\Elon")         
load_known_faces("Hema", r"C:\Users\gayat\FR_project\Hema")

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Process each frame from the video
while True:
    ret, frame = video_capture.read()
    
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Increase the tolerance to 0.5 for stricter matching
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"
        confidence = 0

        # Use the known encoding with the smallest distance to the new encoding
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            confidence = 1 - face_distances[best_match_index]  # Calculate confidence as (1 - face distance)

        if name == "Unknown":
            box_color = (0, 0, 255)  # Red for unknown faces
            text_color = (0, 0, 255)
        else:
            box_color = (0, 255, 0)  # Green for known faces
            text_color = (0, 255, 0)

        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
        label = f"{name} ({confidence:.2%})"
        cv2.putText(frame, label, (left, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release video capture and close windows
video_capture.release()
cv2.destroyAllWindows()
