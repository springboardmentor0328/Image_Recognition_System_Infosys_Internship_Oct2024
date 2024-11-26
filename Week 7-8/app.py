# app.py
import streamlit as st
from capture_faces import register_user
from recognize_faces import recognize_faces

def main():
    st.title("Face Recognition System")

    # Select between the two options
    option = st.selectbox('Choose an option', ['Register New User', 'Recognize Faces'])

    if option == 'Register New User':
        # Name input field
        name = st.text_input('Enter your name:')

        # Only show "Start Registration" button after name is entered
        if name and st.button('Start Registration'):
            register_user(name)  # Pass the name to the register_user function

    elif option == 'Recognize Faces':
        if st.button('Start Recognition'):
            recognize_faces()  # Call the function to start face recognition

if __name__ == "__main__":
    main()

# import streamlit as st
# import capture_faces
# import recognize_faces

# # Main page layout
# st.title("Face Recognition System")

# # User Registration Section
# if st.button("Register New User"):
#     name = st.text_input("Enter your name")
#     if name:
#         capture_faces.register_user()
#     else:
#         st.warning("Please enter your name to proceed.")

# # Face Recognition Section
# if st.button("Recognize Faces"):
#     recognize_faces.recognize_faces()

