# Image_Recognition_System_Infosys_Internship_Oct2024
The image recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.
# Face Recognition System

This project is a face recognition system that captures training data from a user, trains a model to recognize faces, and performs real-time face recognition using OpenCV and Gradio.

## Features
- **Capture and Train Faces:** Captures images from a webcam and saves them to a database, then trains a face recognition model using these images.
- **Real-time Face Recognition:** Recognizes faces using the trained model and displays the name of the recognized user.
- **Database Integration:** User data and image paths are stored in an SQLite database.
- **Web Interface:** A Gradio interface to interact with the system.

## Prerequisites
Before running the system, you need to have the following dependencies installed:
- Python 3.x
- OpenCV
- Gradio
- SQLite3
- PIL (Python Imaging Library)
  
## Directory Structure

The directory structure of the project is as follows:



- `dataset/`: This directory stores all the images captured during the training process.
- `trainer/`: This folder contains the trained face recognition model (usually saved as `trainer.yml`).
- `face_recognition.db`: SQLite database used to store user information (names) and the paths to their captured images.
- `main.py`: The main Python script containing the code to capture training data, train the model, and perform real-time face recognition.
- `README.md`: This file, which provides an overview and instructions for the project.

This structure helps keep the project organized by separating captured data, trained models, and the script that runs the system.

## Libraries Used

This project uses the following libraries:

- **OpenCV** (`opencv-python`): A powerful library used for computer vision tasks such as face detection and real-time recognition.
  - `cv2.CascadeClassifier`: Used to detect faces in images and video streams using **Haar Cascades**. The Haar Cascade classifier is a machine learning-based object detection method used to identify objects in images or video.
  - **Haar Cascade Classifiers**: Pre-trained models that OpenCV uses for face detection. The model used in this project is `haarcascade_frontalface_default.xml`, which is specifically designed for detecting frontal faces.
  - `cv2.face.LBPHFaceRecognizer_create()`: Used for training the face recognition model based on **Local Binary Pattern Histograms (LBPH)**. LBPH is a texture-based feature extraction technique used to capture the unique patterns in the facial structure for recognition.
  
- **Gradio** (`gradio`): A library for creating simple and customizable web-based interfaces. It is used here to build the interface for interacting with the face recognition system.
  
- **SQLite3** (`sqlite3`): A lightweight database library used to store user information (such as names) and paths to the captured face images.

- **Pillow** (`Pillow`): A Python Imaging Library (PIL) fork used for opening, manipulating, and saving images. It is used here to process the captured face images.

- **NumPy** (`numpy`): A fundamental package for scientific computing in Python. It is used for handling arrays, particularly in image processing tasks.

### Installation

To install the required libraries, you can use `pip`:

```bash
pip install opencv-python gradio sqlite3 Pillow numpy





