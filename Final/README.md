# **Face Recognition Project**

This project is a real-time **Face Recognition System** that captures, processes, and recognizes faces using webcam input. Facial images are stored in an Oracle database, processed to generate face encodings, and matched against live video feed for recognition.


## **Features**
- **Image Capture**: Capture and save images directly to an Oracle database via a web interface.
- **Face Encoding**: Process stored images to generate unique 128-dimensional face encodings.
- **Real-Time Recognition**: Recognize faces in real-time using a webcam feed.
- **Database Integration**: Store face images and metadata in an Oracle database.


## **Technologies Used**
- **Python**: Main programming language.
- **Libraries**:
  - `face_recognition`: Face detection and encoding.
  - `OpenCV`: Webcam feed processing and display.
  - `cx_Oracle`: Oracle database connectivity.
  - `pickle`: Storing face encodings for faster recognition.
- **Oracle Database**: For storing images and metadata.
- **Flask**: Web framework for the front-end interface.


## **Setup Instructions**

### **1. Prerequisites**
1. **Install Required Tools**:
   - Oracle Database 11g or higher.
   - Python 3.7 or higher.
   - Oracle SQL Developer for managing the database.

2. **Install Python Libraries**:
   ```bash
   pip install face_recognition opencv-python numpy cx_Oracle flask
   ```

3. **Database Configuration**:
   - Update your Oracle database credentials in `app.py` and `save_encodings.py`:

### **2. Steps to Run the Project**

#### **A. Start the Web Application**
1. Run the Flask app (`app.py`) to capture and store images:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```
3. Enter a username and proceed to capture images using your webcam.  
   - Captured images are stored directly in the Oracle database.  


#### **B. Generate Face Encodings**
Run the `save_encodings.py` script to:
- Retrieve images from the Oracle database.
- Generate 128-dimensional face encodings for each image.
- Save these encodings in a `face_encodings.pkl` file:
   ```bash
   python save_encodings.py
   ```


#### **C. Start Real-Time Face Recognition**
Run the `face_recognition_main.py` script for real-time recognition:
```bash
python face_recognition_main.py
```
This script:
- Reads encodings from `face_encodings.pkl`.
- Opens the webcam feed.
- Recognizes faces in real time, displaying the name and confidence percentage on the screen.

**Press 'q'** to exit the recognition window.


