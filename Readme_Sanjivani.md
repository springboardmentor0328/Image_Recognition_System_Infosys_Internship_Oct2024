# Face Recognition System Using MobileNetV2

The face recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.

This project is a face recognition system developed using Flask, OpenCV, and MobileNetV2, designed to capture and recognize faces in real-time. It extracts facial embeddings from live video streams and matches them against stored data, providing a confidence score for each recognition attempt.

# Components Used
1. Flask: Web server for hosting the user interface and handling backend operations.
2. OpenCV: Used for real-time video capture and face detection(Haar cascade).
3. MobileNetV2: A pre-trained model for extracting facial embeddings.
4. SQLite: Database for storing facial embeddings and associated user data.

# Week-Wise Progress
Week 1-2: Face detection using Haarcascade. Demonstrated real-time face detection with a webcam and static image detection.

Week 3-4: Integrated MobileNetV2 for extracting facial embeddings. Implemented real-time face recognition with transfer learning and embedding comparison using cosine similarity.

Week 5-6: Enhanced face capturing system with multiple position-specific images, integrating OpenCV and JavaScript for real-time webcam input. Gradio was integrated for the face recognition UI, though it faced some challenges with face capturing.

Week 7-8: Developed a Flask-based face recognition app, utilizing an SQLite database to store and retrieve facial embeddings for efficient recognition. The system is designed for real-time recognition using the pre-captured embeddings.

Face Recognition System: Contains the main code

# Conclusion
This face recognition system provides a simple yet effective way to register and recognize faces using a webcam and deep learning models. It captures multiple images, processes them to extract facial features, and matches them against a database in real-time.
