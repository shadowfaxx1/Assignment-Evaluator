# app/admin/admin_routes.py
import streamlit as st
from db.database import create_connection
import pandas as pd
import time
from admin.datadisplayer import datashow
from db.resultdb import create_conn
# Hardcoded admin credentials (replace with a more secure method in a production environment)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
session_state = st.session_state


def admin_login():
    # Check if the user is already authenticated as admin
    if getattr(session_state, "is_admin_authenticated", False):
        datashow()
        return

    st.title("Admin Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session_state.is_admin_authenticated = True
            with st.spinner(text='In progress'):
                time.sleep(3)
                st.success('Login successful!')
            admin_home()
        else:
            st.error("Invalid username or password. Please try again.")



def admin_home():
    st.title("Admin Home Page")
    st.write("Welcome to the Admin Home Page! Below is the submission by student")

    # Fetch and display assignment details from the database
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assignments")
        assignments = cursor.fetchall()
        conn.close()

        if assignments:
            # Convert the assignments to a pandas DataFrame for better presentation
            df = pd.DataFrame(assignments, columns=[col[0] for col in cursor.description]).set_index("id")
            markdown_table = df.to_markdown(index=False)

            # Display Markdown table
            st.markdown(markdown_table, unsafe_allow_html=True)
            st.write("Please click on Report button in Nav Bar to view full report ")
        
        else:
            st.write("No assignments found.")
    zonn = create_conn()
    if zonn:
        cur = zonn.cursor()
        cur.execute("select * from student_results")
        finalres = cur.fetchall()
        zonn.close()
        if finalres:
                df = pd.DataFrame(finalres, columns=[col[0] for col in cur.description]).set_index("enrollment_number")
                df.drop(['id'],axis=1)
                st.write(df)
    else:
         print("no final report right now ")

    if session_state.is_admin_authenticated and st.sidebar.button("Reports"):
                datashow()


# Example usage
