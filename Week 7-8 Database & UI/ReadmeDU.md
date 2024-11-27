# Face Recognition and Face Capturing System

This repository contains two Flask-based applications:
1. Face Capturing App – For capturing face images and saving embeddings for future recognition.
2. Face Recognition App – For real-time face recognition using pre-captured embeddings.
   
Both applications are now set up to run on local machine, and Flask is used for creating the user interface. The system is designed to integrate with a database using SQLite for saving and retrieving face embeddings.

# Database

The database is used to store face embeddings and their corresponding labels for efficient matching and retrieval during the recognition process. SQLite is used as it is light weight, faster and efficient to access.

Features
- SQLite Database stores the embeddings and labels.
- Embeddings Table stores each user’s embedding along with the label.
- Allows easy querying of embeddings for recognition.

# User Interface
The user interface is built using Flask, which provides a simple and interactive way to capture images and perform face recognition. It enables easy interaction via a browser interface.

# Requirements:
- python
- tensorflow
- sqlite3
- flask
- opencv
- html/css

