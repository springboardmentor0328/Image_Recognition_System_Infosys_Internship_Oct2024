# Image_Recognition_System_Infosys_Internship_Oct2024
The image recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.

This is a real-time face recognition app built with Python , flask and LBPH. It enables users to register and recognize faces using webcam input.

__Requirements__  
1. Create a virtual environment:  
   `python -m venv venv`<br>
   `venv\Scripts\activate`<br>
2. OpenCV library:  
   `pip install opencv-python opencv-contrib-python`<br>
3. Numpy:  
   `pip install numpy`<br>
4. Flask:  
   `pip install flask`<br>

__Code files and folders__  

**Main Scripts:**  

__app.py:__ Main Flask application.<br>
__face_recognize.py:__ Logic for face recognition and user registration.<br>
__create_data.py:__ Script for manually creating datasets (optional).<br>

**Model Files:**  

__haarcascade_frontalface_default.xml:__ Pre-trained model for face detection.<br>
__face_model.xml:__ Stores the trained face recognition model (generated during training).<br>

**Web Interface Files:**  

__index.html:__ The front-end interface.<br>
__styles.css:__ CSS for styling the interface.<br>
__script.js:__ JavaScript for UI interaction and backend communication.<br>

**Folders:**  

__datasets/:__ Stores face image datasets for registered users (auto-created during registration).<br>

__How to run the app__  

Use command:  
`python app.py`<br>

__Usage instructions__  

__Register a user__  
1. Enter the name of the user in the input box.<br>
2. Click "Register User" then it opens the webcam and starts capturing faces.<br>
3. Once completed, the user will be added to the datasets.<br>

__Start Face Recognition__  
1. Click "Start Face Recognition".<br>
2. The app will display a live webcam feed, highlighting recognized faces and displaying their names.<br>

__Stop Face Recognition__  
Click "Stop Face Recognition" to end the recognition process.<br>




