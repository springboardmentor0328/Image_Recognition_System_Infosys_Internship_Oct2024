import cv2
import os

# Path to save captured images
dataset_path = 'dataset'

# Instruction states
instructions = ["Move Up", "Move Down", "Move Right", "Move Left"]
completed_instructions = {direction: 0 for direction in instructions}  # Track how many images captured

# Define frame size
frame_w, frame_h = 400, 300  # Size of the frame (width, height)

def capture_images(person_name):
    # Create a directory to save images
    save_dir = os.path.join(dataset_path, person_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Set up video capture and load the face detection cascade
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Get video frame width and height for centering the rectangle
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the center of the screen
    frame_x = (frame_width - frame_w) // 2  # Horizontal center
    frame_y = (frame_height - frame_h) // 2  # Vertical center

    # Wait until the face is inside the static frame
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        # Draw the static instruction frame (yellow rectangle) for the user to place their face inside
        cv2.rectangle(frame, (frame_x, frame_y), (frame_x + frame_w, frame_y + frame_h), (0, 255, 255), 2)

        face_inside_frame = False  # Flag to check if face is inside frame

        for (x, y, w, h) in faces:
            # Draw rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Check if the face is inside the static frame (within the bounds)
            if (x + w > frame_x and x < frame_x + frame_w and y + h > frame_y and y < frame_y + frame_h):
                face_inside_frame = True

        # Provide feedback to the user
        if face_inside_frame:
            cv2.putText(frame, "Face detected inside the frame. Capture will start now.", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Follow the instructions to move your face.", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Face Capture", frame)
            break  # Face is inside the frame, break to start guiding and capturing

        else:
            cv2.putText(frame, "Please place your face inside the frame!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Show the frame with the face detection and feedback
        cv2.imshow("Face Capture", frame)

        # Check for 'q' key press to quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Now proceed with the instructions for moving the head

    img_count = 0  # Total image counter across all directions
    instruction_idx = 0  # Track current instruction

    while instruction_idx < len(instructions):
        # Initialize the counter for the current direction (25 images per direction)
        images_for_current_instruction = 0
        
        # Show instruction text
        current_instruction = instructions[instruction_idx]
        print(f"Now performing: {current_instruction}")

        while images_for_current_instruction < 25:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Convert frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            # Draw the static instruction frame (yellow rectangle) for the user to place their face inside
            cv2.rectangle(frame, (frame_x, frame_y), (frame_x + frame_w, frame_y + frame_h), (0, 255, 255), 2)

            face_inside_frame = False  # Flag to check if face is inside frame

            for (x, y, w, h) in faces:
                # Draw rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Check if the face is inside the static frame (within the bounds)
                if (x + w > frame_x and x < frame_x + frame_w and y + h > frame_y and y < frame_y + frame_h):
                    face_inside_frame = True

            # If face is inside the frame, proceed to capture images
            if face_inside_frame:
                # Now check if the user is performing the correct movement for this instruction
                cv2.putText(frame, f"Instruction: {current_instruction}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

                # Check if the user has moved in the required direction
                if current_instruction == "Move Up" and y < 100:
                    images_for_current_instruction += 1
                    cv2.putText(frame, f"Captured {images_for_current_instruction} images", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                elif current_instruction == "Move Down" and y > 200:
                    images_for_current_instruction += 1
                    cv2.putText(frame, f"Captured {images_for_current_instruction} images", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                elif current_instruction == "Move Right" and x < 100:
                    images_for_current_instruction += 1
                    cv2.putText(frame, f"Captured {images_for_current_instruction} images", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                elif current_instruction == "Move Left" and x > 200:
                    images_for_current_instruction += 1
                    cv2.putText(frame, f"Captured {images_for_current_instruction} images", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Save image every time the direction condition is met
                img_path = os.path.join(save_dir, f'{person_name}_{img_count}.jpg')
                cv2.imwrite(img_path, frame)
                print(f"Saved {img_path}")
                img_count += 1

            else:
                cv2.putText(frame, "Please keep your face inside the frame!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Show the frame with feedback
            cv2.imshow("Face Capture", frame)

            # Check for 'q' key press to quit manually
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Move to the next instruction after capturing enough images
        print(f"Captured {images_for_current_instruction} images for {current_instruction}")
        completed_instructions[current_instruction] = images_for_current_instruction
        instruction_idx += 1  # Proceed to next instruction

    # Final message when capturing is complete
    cv2.putText(frame, "All Instructions Complete!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Face Capture", frame)

    # Wait for 1 second and close the window
    cv2.waitKey(1000)  # Wait 1 second to display the "Complete" message
    cap.release()  # Release the video capture
    cv2.destroyAllWindows()  # Close all windows

# Capture images by providing the person's name
if __name__ == "__main__":
    person_name = input("Enter the person's name: ")
    capture_images(person_name)  # Corrected this line to properly call the function
