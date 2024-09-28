import sqlite3
import csv
import os

def export_to_csv(db_path, csv_file_path):
    """
    Export data from SQLite database to a CSV file.

    :param db_path: Path to the SQLite database.
    :param csv_file_path: Path where the CSV file will be saved.
    """
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}. Please check the path.")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query the auctions table to get all data
        cursor.execute("SELECT * FROM auctions")
        data = cursor.fetchall()

        # Fetch column names
        column_names = [description[0] for description in cursor.description]

        # Write data to CSV file
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write column headers
            writer.writerows(data)  # Write data rows

        print(f"Data successfully exported to {csv_file_path}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    db_path = "src/db/auction_data.db" 
    csv_file_path = "src/utils/exported_data.csv" 
    
    export_to_csv(db_path, csv_file_path)
