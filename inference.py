import cv2
import os
import numpy as np

# Path to the dataset directory
data_path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

label_dict = {}

# Load images and labels for training
def load_images_and_labels(data_path):
    images = []
    labels = []
    current_label = 0

    if not os.path.exists(data_path):
        print(f"Directory '{data_path}' does not exist. Please check the path or create the folder.")
        return images, labels, label_dict

    for person_name in os.listdir(data_path):
        person_folder = os.path.join(data_path, person_name)
        if os.path.isdir(person_folder):
            label_dict[current_label] = person_name
            for img_name in os.listdir(person_folder):
                img_path = os.path.join(person_folder, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    faces = face_cascade.detectMultiScale(img, 1.1, 5)
                    for (x, y, w, h) in faces:
                        face = cv2.resize(img[y:y+h, x:x+w], (200, 200))
                        images.append(face)
                        labels.append(current_label)
                else:
                    print(f"Warning: Unable to read image at {img_path}")
            current_label += 1

    return images, np.array(labels, dtype=np.int32), label_dict

# Function to train the recognizer
def train_model():
    images, labels, label_dict = load_images_and_labels(data_path)
    if len(images) > 0 and labels.size > 0:
        recognizer.train(images, labels)
        print("Model training complete.")
    else:
        print("No data to train on. Check the dataset directory and images.")

# Real-time face recognition
def recognize_faces():
    cap = cv2.VideoCapture(0)
    frame_skip = 2  # Process every 2nd frame to reduce lag
    frame_count = 0
    unknown_threshold = 50  # Set threshold for recognizing unknown faces

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # Skip this frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)  # Adjusted parameters for speed

        for (x, y, w, h) in faces:
            face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label, confidence = recognizer.predict(face)

            # Check confidence level to determine if face is recognized or "Unknown"
            if confidence < unknown_threshold:
                label_text = label_dict.get(label, "Unknown")
                text = f"{label_text} ({100 - confidence:.2f}%)"
                color = (0, 255, 0)  # Green for recognized face
            else:
                text = "Unknown"
                color = (0, 0, 255)  # Red for unknown face

            # Draw bounding box and text
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Face Recognition', frame)

        # Press 'Esc' to exit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(images) > 0 and labels.size > 0:
        recognize_faces()
    else:
        print("Face recognizer is not trained due to insufficient or missing training data.")
