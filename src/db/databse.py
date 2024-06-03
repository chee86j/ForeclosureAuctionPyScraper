#   Database functions for creating and inserting into the SQLite database
#   It connects to the SQLite database and creates a table if it doesn't exist
import sqlite3

class Database:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.create_table()

    def create_table(self):
        self.connection.execute('''CREATE TABLE IF NOT EXISTS auctions
                            (case_number TEXT, sale_date TEXT, property_address TEXT, status TEXT)''')
        self.connection.commit()

    def insert_auction(self, item):
        self.connection.execute('INSERT INTO auctions (case_number, sale_date, property_address, status) VALUES (?, ?, ?, ?)',
                                (item['case_number'], item['sale_date'], item['property_address'], item['status']))
        self.connection.commit()

    def close(self):
        self.connection.close()
