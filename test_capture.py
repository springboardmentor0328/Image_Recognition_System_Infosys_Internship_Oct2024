# test_capture.py
import capture  # Import the capture module where capture_images is defined

# Run the capture function directly
try:
    capture.capture_images("test_user")
    print("Capture function ran successfully.")
except Exception as e:
    print(f"Error in capture_images function: {e}")
