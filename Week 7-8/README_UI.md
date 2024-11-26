# Face Recognition System
This project implements a face recognition system using Python, OpenCV, and the face_recognition library. The system is capable of recognizing and verifying faces in real-time through a user-friendly interface built with Streamlit. It also integrates with an SQLite3 database to manage and store user data, including face encodings, for future recognition.

## Features
Real-Time Face Recognition: Detect and recognize faces using a webcam or image input.

Face Registration: Register new faces by capturing images and saving face encodings to the database.

User Management: Easily store, update, and manage user details in the SQLite database.

UI with Streamlit: Interactive, web-based user interface to interact with the face recognition system.

Database Integration: SQLite3 used for securely storing user information and face encodings for fast recognition.

## Technologies Used

Python: Programming language used for the implementation.

OpenCV: Used for image processing and computer vision tasks such as face detection.

face_recognition: A library built on top of dlib, used for face recognition and encoding.

Streamlit: A framework for building the front-end UI.

SQLite3: A lightweight, serverless database for storing face encodings and user information.
