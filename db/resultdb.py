# app/db/database.py
import sqlite3
from sqlite3 import Error
from datetime import datetime
import json 

DATABASE_FILE = "result_db.sqlite"

def create_conn():
    """Create a database connection to SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        print(f"Connected to the database: {DATABASE_FILE}")
    except Error as e:
        print(f"Error connecting to the database: {e}")

    return conn

def creating(conn):
    """Create necessary tables in the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                enrollment_number TEXT,
                plagiarism REAL,
                informative TEXT,
                sentiment TEXT,
                language_complexity TEXT,
                assignment_structure TEXT,
                wordcount INTEGER,
                timestamp DATETIME
            );
        """)

        conn.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating tables: {e}")

def saving(conn, name, enrollment_number, plagiarism, informative, sentiment, 
                    language_complexity, assignment_structure, wordcount):
    """Save result details to the database."""
    try:

        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        informative = json.dumps(informative)
        cursor.execute("""
            INSERT INTO results (
                name, enrollment_number, plagiarism, informative, sentiment,
                language_complexity, assignment_structure, wordcount, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            name, enrollment_number, plagiarism, informative, sentiment,
            language_complexity, assignment_structure, wordcount, timestamp
        ))

        conn.commit()
        print("result details saved to the database.")
    except Error as e:
        print(f"Error saving result details: {e}")

def initializedb():
    """Initialize the database."""
    connection = create_conn()
    if connection is not None:
        creating(connection)
        connection.close()

if __name__ == "__main__":
    initializedb()
