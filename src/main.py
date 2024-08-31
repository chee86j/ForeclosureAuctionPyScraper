from src.scraper.scraper import parse_page_selenium
from src.db.database import connect_db, create_table, insert_data, close_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    url = "https://salesweb.civilview.com/Sales/SalesSearch?countyId=9&page=1"
    
    data = parse_page_selenium(url)
    if data:
        conn = connect_db()
        if conn:
            create_table(conn)
            insert_data(conn, data)
            close_db(conn)
        else:
            logging.error("Failed to connect to the database.")
    else:
        logging.warning("No data scraped.")

if __name__ == "__main__":
    main()
