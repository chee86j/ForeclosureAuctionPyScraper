#   Database functions for creating and inserting into the SQLite database
#   It connects to the SQLite database and creates a table if it doesn't exist
import sqlite3
import logging

class Database:
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            return sqlite3.connect(self.database_path)
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            return None

    def create_table(self):
        try:
            with self.connection:
                self.connection.execute('''
                    CREATE TABLE IF NOT EXISTS auctions (
                        details_url TEXT,
                        case_number TEXT, 
                        sale_date TEXT, 
                        property_address TEXT, 
                        status TEXT, 
                        attorney_name TEXT, 
                        plaintiff_name TEXT
                    )
                ''')
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")

    def insert_auction(self, item):
        try:
            with self.connection:
                self.connection.execute('''
                    INSERT INTO auctions (details_url, case_number, sale_date, property_address, status, attorney_name, plaintiff_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (item.get('details_url'), item['case_number'], item['sale_date'], item['property_address'], item['status'], item.get('attorney_name', 'Not Available'), 
                item.get('plaintiff_name', 'Not Available')))
        except sqlite3.IntegrityError:
            logging.error(f"Duplicate entry found for case number: {item['case_number']}")

    def close(self):
        if self.connection:
            self.connection.close()
