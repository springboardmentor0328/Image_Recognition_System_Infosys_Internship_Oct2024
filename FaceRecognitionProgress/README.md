# Face Recognition System

This project is a Python-based face recognition system that uses the `face_recognition` library to recognize faces in real-time using a webcam. It also includes a script to generate and store face encodings from a dataset of images.

## Features
- **Real-Time Face Recognition**:
  - Detects faces from webcam video streams.
  - Identifies recognized faces and labels them with names and confidence percentages.
  - Displays a bounding box around detected faces:
    - **Green**: Recognized face.
    - **Red**: Unrecognized face.
- **Encoding Generation**:
  - Processes images from a dataset (organized in subfolders by person names).
  - Generates face encodings and saves them in a `.pkl` file for efficient recognition.

### Python Libraries
- `face_recognition`
- `pickle`
- `cv2` (OpenCV)
- `numpy`

