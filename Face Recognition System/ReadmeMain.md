# Face Recognition System

Overview
This project is a web-based face recognition system using Flask, OpenCV, and TensorFlow. It captures face images from a live video feed, processes them to extract facial embeddings using MobileNetV2, and stores the embeddings in an SQLite database for future recognition. The system then matches the live camera feed against previously captured faces, displaying the recognized person with a confidence score.

# Components
1. Flask Web Server: A lightweight server used to serve the web interface for user interaction.
2. OpenCV: Handles video capture, face detection, and image processing.
3. MobileNetV2: A pre-trained deep learning model used to extract facial embeddings.
4. SQLite Database: Stores the facial embeddings associated with each user.

# Features
- User Registration: Allows new user to register their usename and face.
- Guided Face Capture: The user is instructed to align their face and move in various directions. Faces are captured and stored in the system.
- Face Recognition: After the user registration, the system recognizes faces from the live video feed and matches them to the stored embeddings.
- Confidence Score: The system displays the confidence score of the face recognition process, indicating the likelihood of a correct match.
- Real-Time Video Feed: Displays the live video stream with bounding boxes around detected faces and their names or "Unknown" if no match is found.
- Lightweight model: Uses lightweight model for face detection as well as face recognition.

# Folder Explaination
- app.py: The main application script where the server, face detection, and recognition logic reside.
- captured_faces/: Folder where the captured face images are stored by user and later deleted.
- embeddings.db: SQLite database file where facial embeddings are stored.
- templates/: Contain all html pages required for the smooth UI

# How it works?
1. Face Detection: OpenCV's Haar Cascade Classifier detects faces in the camera feed.
2. Face Embeddings: MobileNetV2 extracts embeddings from detected faces. These embeddings are a numerical representation of the face.
3. Database Storage: The embeddings, along with the username, are stored in an SQLite database.
4. Face Matching: During recognition, the system computes the cosine similarity between the current face's embedding and those stored in the database. If a match is found with a confidence score above 0.85, the user’s name is displayed.
5. Confidence Score: The confidence score indicates how closely the detected face matches with the stored face. A score above 0.85 is considered a high match.

To run the code (make sure to create captured_faces folder):
  python app.py

# Troubleshooting
- No face detected: Ensure that your face is properly aligned within the center region on the screen.
- Database issues: Ensure that the SQLite database file (embeddings.db) is accessible and not locked by another process.
- Camera issues: Ensure that the camera is correctly connected and accessible by OpenCV.

# Conclusion
This face recognition system provides a simple yet effective way to register and recognize faces using a webcam and deep learning models. It is lightweight, efficientand user friendly. It captures multiple images, processes them to extract facial features, and matches them against a database in real-time.
