#   Database functions for creating and inserting into the SQLite database
#   It connects to the SQLite database and creates a table if it doesn't exist
import sqlite3
import logging

# Configure logging
logging.basicConfig(filename='database.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

DATABASE_NAME = 'auction_data.db'

def connect_db():
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        logging.info(f"Connected to the database: {DATABASE_NAME}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def create_table(conn):
    """Create the auctions table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auctions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detail_link TEXT,
                sheriff_number TEXT,
                status_date TEXT,
                plaintiff TEXT,
                defendant TEXT,
                address TEXT
            )
        ''')
        conn.commit()
        logging.info("auctions table created or already exists.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

def insert_data(conn, data):
    """Insert data into the auctions table."""
    try:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO auctions (detail_link, sheriff_number, status_date, plaintiff, defendant, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [(entry['detail_link'], entry['sheriff_number'], entry['status_date'], entry['plaintiff'], entry['defendant'], entry['address']) for entry in data])
        conn.commit()
        logging.info(f"Inserted {cursor.rowcount} rows into the auctions table.")
    except sqlite3.Error as e:
        logging.error(f"Error inserting data: {e}")

def close_db(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        logging.info("Database connection closed.")


