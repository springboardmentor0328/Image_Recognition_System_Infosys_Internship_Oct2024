# Image_Recognition_System_Infosys_Internship_Oct2024
The image recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.

# Real-time Face Recognition System

This project is a face recognition and user registration system built using Python, OpenCV, face recognition library, Streamlit, and SQLite3. The system allows for new user registration and face recognition, with a simple web UI built using Streamlit. The project is divided into different weeks, with each week focusing on a specific functionality.

## Project Structure

The project is divided into the following folders based on the weeks:

### Week 1-2: Face Detection using Haarcascades
In this section, we implemented face detection using OpenCV and Haarcascades. The code detects faces in images or video streams and marks them with bounding boxes. The face detection model used here is pre-trained, making it suitable for real-time applications.

**Key Technologies Used:**
- Python
- OpenCV (Haarcascades)

### Week 3-4: Face Recognition using `face_recognition` Library
This part of the project focuses on face recognition using the `face_recognition` library, which provides a simple API for recognizing and encoding faces. We used this library to identify faces and compare them with previously stored face encodings for recognition.

**Key Technologies Used:**
- Python
- `face_recognition` Library

### Week 5-6: Database Integration with SQLite3
In this section, we integrated an SQLite3 database to store user details during registration. New users can register with their name and face image, which are stored in the database for future recognition.

**Key Technologies Used:**
- Python
- face_recognition Library
- SQLite3

### Week 7-8: Web UI using Streamlit
In the final weeks, we built a simple web app using Streamlit. The UI allows users to select between two main options:
1. **Face Recognition:** Users use their camera for recognition, and the system will attempt to match the face with registered users in the database.
2. **New User Registration:** New users can register by providing their names, the live camera feed captures images from different face angles, which will be stored in the database for future recognition.

**Key Technologies Used:**
- Python
- face_recognition Library
- OpenCV
- Streamlit
- SQLite3


