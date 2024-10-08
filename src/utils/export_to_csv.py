import logging
import sqlite3
import pandas as pd

# Export the data from the SQLite database to a CSV file without Duplicates
def export_data_to_csv(db_file, csv_file):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        
        # Define the query to select all columns from the auctions table
        query = 'SELECT DISTINCT * FROM auctions'
        
        # Query the auctions table and load the data into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Export the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)
        
        # Close the connection
        conn.close()
        print(f"Data has been exported to {csv_file}")
        logging.info(f"Data exported to {csv_file} without duplicates.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Failed to export data: {e}")

if __name__ == "__main__":
    db_file = 'auction_data.db'  # The SQLite database file
    csv_file = 'auction_data.csv'  # The output CSV file
    
    export_data_to_csv(db_file, csv_file)
