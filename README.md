# Image_Recognition_System_Infosys_Internship_Oct2024
The image recognition project aims to develop a system capable of recognising individuals using a laptop's camera. This system leverages computer vision techniques to capture real-time images and process them for face identification.
# Face Recognition Project

This project is focused on building a comprehensive face recognition system, leveraging various frameworks and methodologies for face detection, face recognition, and real-time video processing. Below is a breakdown of the project from Week 1 to Week 8.

---

## **Project Overview**

This project integrates **OpenCV**, **dlib**, and **face_recognition** libraries to implement functionalities like:  
1. **Face Detection** using Haar Cascades and DNN models.  
2. **Face Recognition** with dlib's face embeddings and OpenCV.  
3. Real-time face recognition using a webcam.  
4. A Gradio-based interface for face registration, recognition, and dataset management.

---

## **Weeks 1 & 2: Face Detection**  
### Objectives:
- Load images and videos for face detection.
- Explore Haar Cascades and DNN-based approaches.

### Highlights:
1. **Haar Cascade Classifier**  
   - Detected faces in static images with bounding boxes.  
   - Example: Detected 6 faces in `PersonE.jpg`.  

2. **DNN-Based Detection**  
   - Leveraged a pre-trained SSD (Single Shot Multibox Detector) with Caffe for better accuracy.
   - Applied detection on static images and video frames with bounding boxes drawn on detected faces.

---

## **Weeks 3 & 4: Face Recognition with dlib**  
### Objectives:
- Compute face embeddings for recognition.  
- Implement face matching between reference and test images.  

### Highlights:
1. Used dlib's **ResNet-based face recognition model** and 68-point face landmark detector.  
2. Matched a reference image (`Virat1.jpg`) with test images (`Virat6.jpg`, `dhoni.jpg`), and categorized results as:
   - **Match**: When the Euclidean distance < 0.4.  
   - **Not Match**: When the Euclidean distance ≥ 0.4.  

---

## **Weeks 5-8: Advanced Features with Gradio**  
### Objectives:
- Enable face registration via webcam.  
- Real-time face recognition with a friendly UI.  

### Highlights:
1. **Face Registration**  
   - Captured and saved face images dynamically using a webcam.  
   - Utilized Haar Cascades for face cropping and saving in a structured dataset.

2. **Real-Time Face Recognition**  
   - Encoded known faces and matched them against live webcam frames.  
   - Displayed recognition results (bounding boxes, names, confidence levels).

3. **Gradio Integration**  
   - Built a **tabbed interface** for:
     - Registering new faces.
     - Loading known faces from the dataset.
     - Real-time recognition.

---

## **Technologies Used**

- **Libraries**: OpenCV, dlib, face_recognition, Gradio, NumPy, Matplotlib  
- **Tools**: Python, Google Colab, Webcam Integration  
- **Models**:  
  - Haar Cascade for face detection.  
  - SSD with ResNet backbone for DNN-based detection.  
  - dlib's ResNet model for face recognition.

---

## **Results & Observations**

1. Haar Cascades worked well for simple images but struggled with low-light or complex backgrounds.  
2. DNN-based detection provided better accuracy and was effective for real-time video processing.  
3. dlib's embeddings proved to be highly robust for recognition tasks.  
4. Gradio simplified UI/UX, making the application user-friendly and interactive.

---

## **Conclusion**

This project successfully demonstrates the capabilities of computer vision for face detection and recognition. It combines robust detection and recognition techniques, providing an extensible framework for real-world applications like attendance systems, security, and access control. The integration with Gradio makes it scalable and user-friendly for non-technical users.  

Future improvements could include:  
- Incorporating deep learning-based models for enhanced accuracy.  
- Extending support to recognize faces in large crowds.  
- Exploring edge devices for deploying real-time recognition.  

--- 
