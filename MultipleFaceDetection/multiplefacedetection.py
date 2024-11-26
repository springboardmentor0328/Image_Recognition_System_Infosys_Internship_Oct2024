import cv2

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the image from file
image_path = r"Replace with your image file name or path"
image = cv2.imread(image_path)

# Check if image was loaded successfully
if image is None:
    print("Error: Could not read the image.")
    exit()

# Convert the image to grayscale for better face detection
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Display the resulting image with rectangles around detected faces
cv2.imshow('Face Detection', image)

# Wait for a key press and close the displayed window
cv2.waitKey(0)
cv2.destroyAllWindows()