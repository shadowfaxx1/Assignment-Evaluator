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
            # fx and df names are mixed up follow up and resolve next thing also create a seperate page for final result 
        st.subheader("Live Graphs")
        st.plotly_chart(px.box(df, x="enrollment", y="polarity", title="Box Plot of Polarity").update_layout(showlegend=False))
        st.plotly_chart(px.histogram(df, x="subjectivity", title="Count Plot of Subjectivity").update_layout(showlegend=False))
        st.plotly_chart(px.violin(df, x="enrollment", y="word_count", color=df['senitiment'], box=True, points="all",
                                title="Violin Plot of Word Count by Sentiment").update_layout(showlegend=False))
        st.plotly_chart(px.scatter(df, x="average_sentence", y="complex_percentage", marginal_x="histogram", marginal_y="histogram",
                                    title="Kernel Density Estimate (KDE) Plot of Average Sentence vs. Complex Percentage").update_layout(showlegend=False))
        st.plotly_chart(px.violin(fx, x="name", y="plagiarism", color="assignment_structure", box=True, points="all",
                                title="Violin Plot of Plagiarism by Assignment Structure with Hue").update_layout(showlegend=False))
        st.plotly_chart(px.box(df, x="enrollment", y="fog_index", color="negative_word",
                                title="Box Plot of Fog Index with Hue for Negative Word (Binary)").update_layout(showlegend=False))
        st.plotly_chart(px.line(df, x='enrollment', y='polarity', title='Line Chart of Sentiment Polarity').update_layout(showlegend=False))
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
 


