# New User Face Capture
The system allows to captures face images from the user's webcam using a central and position-specific approach. It uses OpenCV for face detection and JavaScript to handle video streaming in the browser. The system allows capturing face images in multiple positions, storing them with a naming convention, and also offers a feature to delete specific images based on user input.
The model is also improved with minor fine tunning for better performance and User Interface is also done using gradio. The integration of gradio was sucessful with face recognition but had several issue while integrating with face capturing.

The following .ipynb file contains code for new user face capturing, model improvement and gradio integration.

Feature:
- Face detection using Haarcascade
- Clear instruction about position while face capturing
- Allows user to delete defected entries.

Requirements:
- Google colab
- Ipython
- numpy
- PIL
- base64

# User Interface
Gradio is a Python library that allows users to quickly create and share user interfaces for machine learning models, enabling real-time interaction with inputs and outputs. 
It allows real-time interface streams webcam input, processes each frame to recognize faces, and displays the results. Bounding boxes and labels with confidence scores are drawn on the recognized faces in real time.

Requirements
- gradio
- gradio-webrtc
