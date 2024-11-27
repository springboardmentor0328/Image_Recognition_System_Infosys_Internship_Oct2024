import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("Capture Face Data")
name=input("Enter Name:\n")
count = 0
while True:
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("Capture Face Data", frame)
    
    # Detect face using Haarcascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw green rectangle around face and save image
    for (x, y, w, h) in faces:
        if count < 50:  # Only save the first 50 images
            count += 1
            face = frame[y:y+h, x:x+w]
            cv2.imwrite(f"D:\Python Codes Clg\infosys\\{name}\\{name}.{str(count)}.jpg", face)
        
        # Draw green rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Show the frame with the rectangle
    cv2.imshow("Capture Face Data", frame)
    
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC to exit
        break

cam.release()
cv2.destroyAllWindows()
