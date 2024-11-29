# Image_Recognition_System_Infosys_Internship_Oct2024
The image recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.

This is a real-time face recognition app built with Python , streamlit and LBPH. It enables users to register and recognize faces using webcam input.

Requirements

Create a virtual environment:
python -m venv venv
venv\Scripts\activate
OpenCV library:
pip install opencv-python opencv-contrib-python
Numpy:
pip install numpy
streamlit:
pip install streamlit
Code files and folders

Main Scripts:

app.py: Main streamlit application.
face_recognize.py: Logic for face recognition and user registration.
create_data.py: Script for manually creating datasets (optional).

Model Files:

haarcascade_frontalface_default.xml: Pre-trained model for face detection.
face_model.xml: Stores the trained face recognition model (generated during training).

Folders:

datasets/: Stores face image datasets for registered users (auto-created during registration).

How to run the app

Use command:
python app.py

Usage instructions

Register a user

Enter the name of the user in the input box.
Click "Register User" then it opens the webcam and starts capturing faces.
Once completed, the user will be added to the datasets.
Start Face Recognition

Click "Start Face Recognition".
The app will display a live webcam feed, highlighting recognized faces and displaying their names.
Stop Face Recognition
Click "Stop Face Recognition" to end the recognition process.
