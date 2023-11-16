# app/admin/admin_routes.py
import streamlit as st
from db.database import create_connection
import pandas as pd
import time
from admin.datadisplayer import datashow
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
            # styled_df = (
            #     df.style
            #     .set_properties(**{'text-align': 'left'})
            #     .background_gradient(cmap='viridis')
            #     .bar(color='black')
            #     .format({'YourColumn': '{:,.2f}'})
            #     .set_caption('Your Custom Caption')
            #     .set_table_styles([
            #         {'selector': 'th', 'props': [('font-size', '16px'), ('color', 'white'), ('background-color', 'black')]},
            #         {'selector': 'td', 'props': [('color', 'white'), ('background-color', 'black')]}
            #     ])
            # )
            # st.dataframe(df.style.set_properties(**{'text-align': 'left'}))
            # st.dataframe(styled_df)
            markdown_table = df.to_markdown(index=False)

            # Display Markdown table
            st.markdown(markdown_table, unsafe_allow_html=True)
            st.write("Please click on Report button in Nav Bar to view full report ")
        
        else:
            st.write("No assignments found.")
    if session_state.is_admin_authenticated and st.sidebar.button("Reports"):
                datashow()


# Example usage
