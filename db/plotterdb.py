import sqlite3
from sqlite3 import Error
from datetime import datetime

DATABASE_FILE = "plotterdb.sqlite"

def con_create():
    """Create a database connection to SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        print(f"Connected to the database: {DATABASE_FILE}")
    except Error as e:
        print(f"Error connecting to the database: {e}")

    return conn

def maketable(conn):
    """Create necessary tables in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plotter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment TEXT,
                postiveword INT,
                negativeword INT,
                polarity FLOAT,
                subjectivity FLOAT,
                average_sentence FLOAT,
                complex_percentage FLOAT,
                fog_index FLOAT,
                average_words INT,
                complex_count INT,
                word_count INT,
                syllable_count INT
            );
        """)

        conn.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating tables: {e}")

def save_ass(conn, enrollment, pos, neg, pol, subj, avg_sent, complex_words, fog_index, avg_words, complex_count, word_count, syllable_count):
    """Save assignment details to the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO plotter (
                enrollment, postiveword, negativeword, polarity, subjectivity, 
                average_sentence, complex_percentage, fog_index, average_words,
                complex_count, word_count, syllable_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            enrollment, pos, neg, pol, subj, avg_sent, complex_words, fog_index,
            avg_words, complex_count, word_count, syllable_count
        ))
        conn.commit()
        print("Assignment details saved to the database.")
    except Error as e:
        print(f"Error saving assignment details: {e}")

def inital():
    """Initialize the database."""
    connection = con_create()
    if connection is not None:
        maketable(connection)
        connection.close()

if __name__ == "__main__":
    inital()
