from email import generator
import sys
import cv2
from flask import Response
import numpy as np
import os
import time
class FaceRecognizer:
    def __init__(self, haar_file='haarcascade_frontalface_default.xml', dataset_dir='datasets'):
        # Initialize face recognizer
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.face_cascade = cv2.CascadeClassifier(haar_file)
        self.dataset_dir = dataset_dir
        self.names = {}  # Maps user IDs to names
        self.width, self.height = 130, 100  # Resize dimensions for training images

        # Load existing dataset for training
        self.load_dataset()

    def load_dataset(self):
        """Loads images from the dataset directory and trains the recognizer model."""
        images, labels = [], []
        id = 0

        # Traverse through dataset directory and load images
        for subdir in os.listdir(self.dataset_dir):
            if os.path.isdir(os.path.join(self.dataset_dir, subdir)):
                self.names[id] = subdir
                subject_path = os.path.join(self.dataset_dir, subdir)
                for filename in os.listdir(subject_path):
                    img_path = os.path.join(subject_path, filename)
                    img = cv2.imread(img_path, 0)
                    if img is not None:
                        img_resized = cv2.resize(img, (self.width, self.height))
                        images.append(img_resized)
                        labels.append(id)
                id += 1

        # Convert images and labels lists to numpy arrays
        images, labels = np.array(images), np.array(labels)

        # Train the model if there are any images
        if len(images) > 0:
            self.model.train(images, labels)

    def register_new_user(self, username):
        """Registers a new user by capturing images from the webcam."""
        user_path = os.path.join(self.dataset_dir, username)
        if not os.path.isdir(user_path):
            os.makedirs(user_path)
        
        webcam = cv2.VideoCapture(0)
        count = 0

        while count < 20:  # Capture 20 images for the new user
            ret, frame = webcam.read()
            if not ret:
                print("Error: Could not access the webcam.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (self.width, self.height))
                
                # Save the image in JPG format
                img_path = os.path.join(user_path, f"{count}.jpg")
                cv2.imwrite(img_path, face_resized)
                count += 1

                # Print progress to the console
                print(f"Captured {count}/20 images for user '{username}'.")

                # Draw a rectangle around the face and display it
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, f"Capturing {count}/20", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Registering New User", frame)

                if count >= 20:
                    break

            # Exit loop if 'q' is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                print("Registration canceled by user.")
                break

        # Release the webcam and close OpenCV windows
        webcam.release()
        cv2.destroyAllWindows()

        # Re-train the model with new data
        self.load_dataset()
        print(f"User '{username}' registered successfully!")

    def register_user_stream(self, username):
        """Stream real-time face registration progress."""
        try:
            user_path = os.path.join(self.dataset_dir, username)
            if not os.path.isdir(user_path):
                os.makedirs(user_path)

            webcam = cv2.VideoCapture(0)
            if not webcam.isOpened():
                yield "data: Error - Could not access the webcam\n\n"
                return

            count = 0
            while count < 20:
                ret, frame = webcam.read()
                if not ret:
                    yield "data: Error - Failed to read from webcam\n\n"
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = gray[y:y + h, x:x + w]
                    face_resized = cv2.resize(face, (self.width, self.height))
                    
                    # Save the image
                    img_path = os.path.join(user_path, f"{count}.jpg")
                    cv2.imwrite(img_path, face_resized)
                    count += 1

                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Add progress text on the frame
                    label_text = f"Capturing {count}/20"
                    cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # Display the frame (optional)
                    cv2.imshow("Registering New User", frame)

                    # Send progress update to client
                    yield f"data: Captured {count}/20 images\n\n"

                    if count >= 20:
                        break

                         
                # Exit loop if 'q' is pressed
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    yield "data: Registration canceled by user\n\n"
                    break

                time.sleep(0.1)

            webcam.release()
            cv2.destroyAllWindows()
            yield "data: Registration complete\n\n"  

        except Exception as e:
            print(f"Error during registration: {e}")
            yield f"data: Error - {str(e)}\n\n"
        finally:
            webcam.release()
            cv2.destroyAllWindows()

    def recognize_faces(self, frame):
        """Detects and recognizes faces in a given frame."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resized = cv2.resize(face, (self.width, self.height))

            # Predict the identity of the face
            label, confidence = self.model.predict(face_resized)
            
            if confidence < 100:  # Adjust threshold as needed
                label_text = f"{self.names[label]} - {confidence:.2f}"
                color = (0, 255, 0)  # Green for recognized faces
            else:
                label_text = "Unknown"
                color = (0, 0, 255)  # Red for unrecognized faces
            
            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

        return frame
