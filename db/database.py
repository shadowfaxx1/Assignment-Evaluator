# app/db/database.py
import sqlite3
from sqlite3 import Error
from datetime import datetime
DATABASE_FILE = "assignment_db.sqlite"

def create_connection():
    """Create a database connection to SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        print(f"Connected to the database: {DATABASE_FILE}")
    except Error as e:
        print(f"Error connecting to the database: {e}")

    return conn

def create_tables(conn):
    """Create necessary tables in the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        enrollment_number TEXT,
        topic TEXT,
        file_path TEXT,
        timestamp DATETIME 
    );
""")


        conn.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating tables: {e}")

def save_assignment(conn, name, enrollment_number, topic, file_path,timestamp):
    """Save assignment details to the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO assignments (name, enrollment_number, topic, file_path,timestamp)
            VALUES (?, ?, ?, ?,?);
        """, (name, enrollment_number, topic, file_path,timestamp))

        conn.commit()
        print("Assignment details saved to the database.")
    except Error as e:
        print(f"Error saving assignment details: {e}")

def initialize_database():
    """Initialize the database."""
    connection = create_connection()
    if connection is not None:
        create_tables(connection)
        connection.close()

if __name__ == "__main__":
    initialize_database()
