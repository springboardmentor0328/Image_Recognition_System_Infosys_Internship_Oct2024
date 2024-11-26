import face_recognition
import pickle
import os

# Directory containing subfolders of images for each person
images_dir = r"replace with your Directory"

# Lists to hold encodings and names
known_face_encodings = []
known_face_names = []

# Loop through each folder in the main directory
for person_name in os.listdir(images_dir):
    person_dir = os.path.join(images_dir, person_name)
    if os.path.isdir(person_dir):  # Only process folders
        # Loop through each image in the person's folder
        for filename in os.listdir(person_dir):
            if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(person_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    known_face_encodings.append(face_encodings[0])
                    known_face_names.append(person_name)  # Assign the folder name as the person's name
# Save the encodings and names to a file using pickle
with open('face_encodings.pkl', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)

print("Encodings saved to face_encodings.pkl.")