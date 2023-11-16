import streamlit as st
from db.resultdb import create_conn
import pandas as pd
import plotly.express as px
from db.plotterdb import con_create
def showgraphs(fx):
        conn= con_create()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plotter")
            result = cursor.fetchall()
            conn.close()

            if result:
                df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
        st.subheader("Live Graphs")

        st.plotly_chart(px.bar(fx, x='name', y='plagiarism', title='Plagiarism Score').update_layout(showlegend=False))
        st.plotly_chart(px.line(df, x='enrollment', y='polarity', title='Sentiment Polarity').update_layout(showlegend=False))
        st.plotly_chart(px.pie(df, names='enrollment', title='Distribution by Enrollment Number').update_layout(showlegend=False))
        st.plotly_chart(px.scatter(df, x='polarity', y='subjectivity', color='enrollment', title='Sentiment Analysis').update_layout(showlegend=False))

def datashow():
    st.title("Reports")
    st.write("This is the student-wise report Section.")
    
    # Establish a connection to the database
    conn = create_conn()
    
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM results")
        result = cursor.fetchall()
        conn.close()

        if result:
            # Convert the assignments to a pandas DataFrame for better presentation
            df = pd.DataFrame(result, columns=[col[0] for col in cursor.description]).set_index("enrollment_number")
            st.dataframe(df)
            showgraphs(df)

        else:
            st.write("No assignments found.")
        
    else:
        print("error")


    # Add content for the student-wise report page here
