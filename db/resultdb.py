import sqlite3
from sqlite3 import Error
from datetime import datetime

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

def create_results_table(conn):
    """Create the 'results' table in the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                enrollment_number TEXT,
                plagiarism FLOAT,
                entailment FLOAT,
                contradiction FLOAT,
                sentiment TEXT,
                language_complexity TEXT,
                assignment_structure TEXT,
                wordcount INTEGER,
                timestamp DATETIME
            );
        """)

        conn.commit()
        print("Results table created successfully")
    except Error as e:
        print(f"Error creating 'results' table: {e}")

def create_student_results_table(conn):
    """Create the 'student_results' table in the database."""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                enrollment_number TEXT,
                result TEXT,
                timestamp DATETIME
            );
        """)

        conn.commit()
        print("Student results table created successfully")
    except Error as e:
        print(f"Error creating 'student_results' table: {e}")

def saving(conn, name, enrollment_number, plagiarism, scorejsonentail, scorejsoncontra, sentiment,
           language_complexity, assignment_structure, wordcount):
    """Save result details to the 'results' table."""
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO results (
                name, enrollment_number, plagiarism, entailment, contradiction, sentiment,
                language_complexity, assignment_structure, wordcount, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            name, enrollment_number, plagiarism, scorejsonentail, scorejsoncontra, sentiment,
            language_complexity, assignment_structure, wordcount, timestamp
        ))

        conn.commit()
        print("Result details saved to the 'results' table.")
    except Error as e:
        print(f"Error saving result details to 'results' table: {e}")

def save_student_result(conn, name, enrollment_number, result):
    """Save student result details to the 'student_results' table."""
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO student_results (
                name, enrollment_number, result, timestamp
            )
            VALUES (?, ?, ?, ?);
        """, (
            name, enrollment_number, result, timestamp
        ))

        conn.commit()
        print("Student result details saved to the 'student_results' table.")
    except Error as e:
        print(f"Error saving student result details to 'student_results' table: {e}")

def initializedb():
    """Initialize the database."""
    connection = create_conn()
    if connection is not None:
        create_results_table(connection)
        create_student_results_table(connection)
        connection.close()

if __name__ == "__main__":
    initializedb()
