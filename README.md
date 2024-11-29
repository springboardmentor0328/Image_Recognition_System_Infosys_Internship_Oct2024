

# **Overview**
This project implements a Face Recognition System using Python, OpenCV, and MySQL. It includes user registration, face detection, dataset generation, training a face recognition classifier, and real-time face recognition. The application has a graphical user interface (GUI) built with Tkinter for better usability.

# **Features**

### 1. User Registration

- Users can register by providing their name, age, and address.  
- Data is stored securely in a MySQL database.

### 2. Dataset Generation

- Captures 200 images of a user's face using a webcam.  
- Stores the images in the specified directory for training.

### 3. Face Recognition

- Recognizes registered faces in real-time using the trained model.  
- Displays the user's name and recognition confidence on the webcam feed.

### 4. Training the Classifier

- Trains an LBPH (Local Binary Patterns Histogram) face recognizer using the collected dataset.
### 5. Error Handling

- Provides meaningful error messages for missing details, duplicate registrations, or missing files.

# Prerequisites

## 1. Python
- Python 3.x installed on your system.
## 2. Libraries
- Install the required Python libraries using pip:  
  pip install tkinter mysql-connector-python pillow opencv-python opencv-contrib-python numpy
## 3. MySQL Database
- MySQL server installed and running.
- A database (demo2) with a table (demo) created as follows:

CREATE TABLE demo (  
    id INT PRIMARY KEY,  
    Name VARCHAR(50),  
    Age INT,  
    Address VARCHAR(255)  
);  

## 4. Configuration
Update the config.properties file with your environment-specific details:
- MySQL credentials.
- Paths for the Haar cascade file, data directory, and classifier save path.

# Project Structure
- Main Code File: Contains the Python code for the application.
- Configuration File (config.properties): Stores database credentials, file paths, and error/information messages.
- Data Directory: Stores the images captured during dataset generation.
- Classifier File (classifier.xml): Stores the trained face recognition model.
  
# Usage
## 1. Start the Application
Run the Python script:

python face_recognition.py

## 2. Features
Register a New User
- Click on "Register New User".
- Fill in the form with the user’s details (Name, Age, Address) and submit.
Detect Faces
- Click on "Detect Faces".
- The system will open a webcam feed and detect faces in real time.
Train Classifier
- Click on "Refresh".
- The system will train the face recognition model using the dataset and save the classifier file.

# Configuration Details
config.properties
- Database Configuration: Update db.host, db.user, db.password, db.database, and db.table with your database credentials.
- File Paths:
   haarcascade_path: Path to the Haar cascade XML file for face detection.  
   data_directory: Path to store the captured face images.  
   classifier_savepath: Path to save the trained face recognition model.  
- Messages: Update user-friendly error and information messages as needed.

# Dependencies
Python Libraries:

- tkinter (for GUI)  
- Pillow (for image processing)  
- opencv-python, opencv-contrib-python (for face recognition)  
- mysql-connector-python (for database connection)  
- numpy (for numerical computations)  

External Files:

- Haar cascade XML file (haarcascade_frontalface_default.xml): Used for face detection.  
- Background image (img6.jpg): Optional decorative image for the GUI.  

  
