import cv2

# Load the input image
input_image_path = r"C:\Users\Administrator\Pictures\Screenshot 2024-11-01 003033.jpg"  # Replace with your image path
img = cv2.imread(input_image_path)

# Check if image was loaded correctly
if img is None:
    print("Error loading image")
    exit()

cv2.namedWindow("Capture Face Data")

# Resize the image
img = cv2.resize(img, (640, 480)) 

# Detect face using Haarcascade with adjusted parameters
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Adjust scaleFactor and minNeighbors 
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

count = 0

# Draw green rectangles around detected faces and save images
for (x, y, w, h) in faces:
    if count < 50:  # Only save up to the first 50 faces
        count += 1
        face = img[y:y+h, x:x+w]
        cv2.imwrite(f"dataset/User.{str(count)}.jpg", face)

    # Draw green rectangle around the face
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.imshow("Capture Face Data", img)

# Wait for user to press any key, then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
