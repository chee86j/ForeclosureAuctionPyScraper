#   Database functions for creating and inserting into the SQLite database
#   It connects to the SQLite database and creates a table if it doesn't exist
import sqlite3
import logging

class Database:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.create_table()

    def create_table(self):
    self.connection.execute('''
        CREATE TABLE IF NOT EXISTS auctions (
            case_number TEXT, 
            sale_date TEXT, 
            property_address TEXT, 
            status TEXT, 
            attorney_name TEXT, 
            plaintiff_name TEXT
        )
    ''')
    self.connection.commit()

    # Added Error handling to prevent duplicate entries
    def insert_auction(self, item):
        try:
            self.connection.execute('INSERT INTO auctions (case_number, sale_date, property_address, status) VALUES (?, ?, ?, ?)',
                                    (item['case_number'], item['sale_date'], item['property_address'], item['status']))
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            logging.error(f"Error inserting data: {e}")

    def close(self):
        self.connection.close()

