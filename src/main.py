import sys
import os
import logging
from scraper.scraper import parse_page_selenium
from db.database import connect_db, create_table, insert_data, close_db
from utils.export_to_csv import export_data_to_csv  # Importing the correct function from utils
import pandas as pd
from merge_csv import merge_csv_files  # Import the merge_csv functionality

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def format_zillow_url(address):
    """Convert the address to a Zillow URL format."""
    try:
        formatted_address = address.replace(" ", "-").replace(",", "")
        zillow_url = f"https://www.zillow.com/homes/{formatted_address}_rb/"
        return zillow_url
    except Exception as e:
        logging.error(f"Error formatting Zillow URL for {address}: {e}")
        return None

def main():
    # Step 1: Scrape auction data
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
    
    # Step 2: Export scraped data to CSV
    user_input = input("Do you want to export the data to CSV? (yes/no): ").strip().lower()
    if user_input == "yes":
        db_path = "auction_data.db"
        csv_file_path = "exported_data.csv"
        
        # Export data to CSV using the imported function from utils
        export_data_to_csv(db_path, csv_file_path)
        print(f"The data has been successfully exported to {csv_file_path}")
    else:
        print("Export to CSV skipped.")

    # Step 3: Generate Zillow URLs for the addresses in the exported data
    user_input = input("Do you want to generate Zillow URLs for the addresses in the exported CSV? (yes/no): ").strip().lower()
    if user_input == "yes":
        try:
            data = pd.read_csv(csv_file_path)
            addresses = data['address'].tolist()
            
            results = []
            for address in addresses:
                zillow_url = format_zillow_url(address)
                if zillow_url:
                    results.append({'address': address, 'Zillow URL': zillow_url})
                    logging.info(f"Successfully formatted URL for {address}")
                else:
                    logging.warning(f"Failed to format URL for {address}")

            # Export Zillow URL results to CSV
            csv_file_path_zillow = 'exported_zillow_urls.csv'
            pd.DataFrame(results).to_csv(csv_file_path_zillow, index=False)
            logging.info(f"Zillow URLs have been successfully exported to {csv_file_path_zillow}")
            print(f"Zillow URLs have been successfully exported to {csv_file_path_zillow}")
            
        except Exception as e:
            logging.error(f"Failed to process addresses for Zillow URL generation: {e}")
            sys.exit(f"Failed to process addresses for Zillow URL generation: {e}")
    else:
        print("Zillow URL generation skipped.")

    # Step 4: Merge the auction data with the Zillow URLs
    user_input = input("Do you want to merge the auction data with the Zillow URLs? (yes/no): ").strip().lower()
    if user_input == "yes":
        try:
            merge_csv_files(csv_file_path, csv_file_path_zillow)
        except Exception as e:
            logging.error(f"Failed to merge files: {e}")
            sys.exit(f"Failed to merge files: {e}")
    else:
        print("Merging auction data and Zillow URLs skipped.")

if __name__ == "__main__":
    main()
