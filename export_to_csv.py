import sqlite3
import pandas as pd

def export_data_to_csv(db_file, csv_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Query the auctions table and load the data into a DataFrame
    df = pd.read_sql_query("SELECT * FROM auctions", conn)
    
    # Export the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)
    
    # Close the connection
    conn.close()
    print(f"Data has been exported to {csv_file}")

if __name__ == "__main__":
    db_file = 'auction_data.db'  # The SQLite database file
    csv_file = 'auction_data.csv'  # The output CSV file
    
    export_data_to_csv(db_file, csv_file)
