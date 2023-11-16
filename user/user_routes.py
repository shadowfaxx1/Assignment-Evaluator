# app/user/user_routes.py
# app/user/user_routes.py
import os
import streamlit as st
from db.database import create_connection, save_assignment
from datetime import datetime
from analyzer.utility import utility

import PyPDF2
from io import BytesIO
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

UPLOADS_PATH = "uploads"
# app/user/user_routes.py

# ... (previous imports)
def user_home():
    st.title("Student's Submission page ")
    st.write("Welcome to the Submission Home !")
    # Add a form for users to input their name, enrollment number, topic, and submit their assignment

    name = st.text_input("Enter your name:")
    enrollment_number = st.text_input("Enter your enrollment number:")
    topic = st.text_input("Enter the topic of your assignment:")
    
    uploaded_file = st.file_uploader("Upload your assignment file", type=["pdf", "docx"])
    destination=None

    if st.button("Submit Assignment"):
        if name and enrollment_number and topic and uploaded_file:
            # Save the assignment to the file system
            folder_name = f"{name}_{enrollment_number}"
            save_path = os.path.join(UPLOADS_PATH, folder_name)
            # Create the directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            destination = file_path
            # Save assignment details to the database
            conn = create_connection()
            if conn:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_assignment(conn, name, enrollment_number, topic, file_path, timestamp)
                conn.close()
            st.success(f"Assignment submitted successfully, {name}! Enrollment Number: {enrollment_number}, Topic: {topic}")
            st.balloons()
        else:
            st.warning("Please fill in all the details and upload your assignment.")
    
    if(destination is not None):
        ss = utility()
        result = ss.analyze_sentiment(destination,name,enrollment_number,name)
        
        