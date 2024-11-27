import cv2
import face_recognition
import os
import gradio as gr

# Initialize lists to hold encodings and names
known_face_encodings = []
known_face_names = []

# Function to capture and save a new face
def register_new_face(name, num_images):
    face_classifier = cv2.CascadeClassifier("C:/Users/gayat/Downloads/haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    img_id = 0

    # Capture new images for registration
    while img_id < num_images:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        
        # If a face is detected, save the cropped face
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cropped_face = frame[y:y+h, x:x+w]
                face = cv2.resize(cropped_face, (200, 200))
                file_name_path = f"C:/Users/gayat/FR_project/{name}/{name}.{img_id + 1}.jpg"
                os.makedirs(os.path.dirname(file_name_path), exist_ok=True)
                cv2.imwrite(file_name_path, face)
                img_id += 1
                cv2.imshow("Face Registration", face)
                
        if cv2.waitKey(1) == 13:  # Enter to break
            break

    cap.release()
    cv2.destroyAllWindows()
    return f"Registration completed for {name}"

# Load all known faces from the main directory
def load_all_faces(main_directory="C:/Users/gayat/FR_project"):
    # Clear existing encodings and names to avoid duplication
    known_face_encodings.clear()
    known_face_names.clear()

    for person_name in os.listdir(main_directory):
        person_folder = os.path.join(main_directory, person_name)
        
        if os.path.isdir(person_folder):  # Check if it is a directory
            for image_file in os.listdir(person_folder):
                image_path = os.path.join(person_folder, image_file)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(person_name)

    return "All images loaded successfully!"

# Real-time face recognition with Gradio
def recognize_faces():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            confidence = 0

            # Check if there's a match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]

            # Draw bounding box and label
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            label = f"{name} ({confidence:.2%})"
            cv2.putText(frame, label, (left, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Real-time recognition stopped"

# Create Gradio Interface
register_interface = gr.Interface(
    fn=register_new_face,
    inputs=["text", gr.Number(label="Number of Images")],
    outputs="text",
    title="Register New Face"
)

load_faces_interface = gr.Interface(
    fn=load_all_faces,
    inputs=None,
    outputs="text",
    title="Load All Faces"
)

recognize_interface = gr.Interface(
    fn=recognize_faces,
    inputs=None,
    outputs="text",
    title="Real-Time Face Recognition"
)
# Launch Gradio Interface
gr.TabbedInterface([register_interface, load_faces_interface, recognize_interface], ["Register Face", "Load Faces", "Real-Time Recognition"]).launch()
