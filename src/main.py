from src.scraper.scraper import parse_page_selenium
from src.db.database import connect_db, create_table, insert_data, close_db
from src.utils.send_email import send_email_notification
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Property in a specific area and price below a certain threshold to be considered relevant for notification
def meets_criteria(listing):
    return 'Morristown' in listing['address'] and int(listing.get('price', 0)) < 500000

def main():
    # List of county URLs and corresponding names to scrape
    counties = {
        "Bergen County": "https://salesweb.civilview.com/Sales/SalesSearch?countyId=7&page=1",
        "Morris County": "https://salesweb.civilview.com/Sales/SalesSearch?countyId=9&page=1"
    }
    
    all_data = []

    for county_name, url in counties.items():
        data = parse_page_selenium(url)
        if data:
            all_data.extend(data)  # Collect data from all counties

            # Filter data based on criteria
            new_listings = [listing for listing in data if meets_criteria(listing)]
        
            if new_listings:
                listings_str = "\n\n".join([f"{listing['address']} - ${listing['price']}" for listing in new_listings])
                logging.info(f"New listings found in {county_name}: {listings_str}")
                
                send_email_notification(
                    subject=f'New Foreclosure Auction Listings in {county_name}',
                    body=f"New auction listings found in {county_name}:\n\n{listings_str}",
                    to_email=os.getenv('RECIPIENT_EMAIL')  # Ensure recipient email is set in your .env
                )

    if all_data:
        conn = connect_db()
        if conn:
            create_table(conn)
            insert_data(conn, all_data)
            close_db(conn)
        else:
            logging.error("Failed to connect to the database.")
    else:
        logging.warning("No data scraped.")

if __name__ == "__main__":
    main()
