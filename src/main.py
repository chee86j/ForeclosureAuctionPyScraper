import sys
import os
import logging
from scraper.scraper import parse_page_selenium
from db.database import connect_db, create_table, insert_data, close_db
from utils.export_to_csv import export_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    url = "https://salesweb.civilview.com/Sales/SalesSearch?countyId=9&page=1"

    logging.info(f"Starting to scrape the page: {url}")
    
    data = parse_page_selenium(url)
    
    if data:
        logging.info(f"Scraping completed. {len(data)} listings found.")
        conn = connect_db()
        if conn:
            create_table(conn)
            insert_data(conn, data)
            close_db(conn)
        else:
            logging.error("Failed to connect to the database.")
    else:
        logging.warning("No data scraped.")
        return  # Exit if no data was scraped
    
    # Ask the user if they want to export data to CSV
    user_input = input("Do you want to export the data to CSV? (yes/no): ").strip().lower()
    if user_input == "yes":
        db_path = "auction_data.db"
        csv_file_path = "exported_data.csv"
        
        # Export data to CSV
        export_to_csv(db_path, csv_file_path)
        print(f"The data has been successfully exported to {csv_file_path}")
    else:
        print("Export to CSV skipped.")

if __name__ == "__main__":
    main()
