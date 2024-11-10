import cv2
import os
import numpy as np

# Path to the dataset directory
data_path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load images and labels for training
def load_images_and_labels(data_path):
    images = []
    labels = []
    label_dict = {}
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
                    faces = face_cascade.detectMultiScale(img, 1.04, 7)
                    for (x, y, w, h) in faces:
                        face = cv2.resize(img[y:y+h, x:x+w], (200, 200))
                        images.append(face)
                        labels.append(current_label)
                else:
                    print(f"Warning: Unable to read image at {img_path}")
            current_label += 1

    return images, np.array(labels, dtype=np.int32), label_dict

# Train the recognizer
images, labels, label_dict = load_images_and_labels(data_path)
if len(images) > 0 and labels.size > 0:
    recognizer.train(images, labels)
    print("Training complete.")
else:
    print("No data to train on. Check the dataset directory and images.")

# Real-time face recognition
def recognize_faces():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: Empty frame captured.")
            continue  # Skip to the next frame if capturing fails

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            face = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
            label, confidence = recognizer.predict(face)
            label_text = label_dict.get(label, "Unknown")
            text = f"{label_text} ({confidence:.2f}%)"
            
            color = (0, 255, 255) if confidence > 50 else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(images) > 0 and labels.size > 0:
        recognize_faces()
    else:
        print("Face recognizer is not trained due to insufficient or missing training data.")
