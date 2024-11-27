# Face Recognition 

MobileNetV2 is a lightweight, efficient convolutional neural network architecture designed for mobile and embedded vision applications. It uses depthwise separable convolutions and an inverted residual structure with linear bottlenecks to achieve high accuracy with reduced computational cost, making it ideal for resource-constrained devices. It is a pre trained model used for feature extraction via transfer learning.
Features:
- Real-Time Video Stream: Captures live video input using the webcam for real-time face recognition.
- Precomputed Embeddings: Saves and retrieves embeddings from an Excel file to avoid redundant computation.
- Transfer Learning with MobileNetV2: Utilizes MobileNetV2 pre-trained on ImageNet for feature extraction, leveraging transfer learning for improved efficiency.
- Embedding Comparison: Computes cosine similarity between live embeddings and known embeddings to identify individuals.
- Confidence Threshold: Recognizes individuals based on a defined similarity threshold for accurate results.
- Dynamic Overlay: Displays names and similarity scores in the video feed with a bounding box.

Requirements:
- TensorFlow/Keras, NumPy, OpenCV, Pandas, Scikit-learn

The code is implemented on Google Colab platform. The code is tailored to work on colab as one cannot directly access local hardware on this platform. Hence, it might need a lot of modification to work on a local system.
