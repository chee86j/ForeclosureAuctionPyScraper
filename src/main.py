# Entry point for app to run the scraper and store the data in the database
# & paginated data
from scraper.scraper import fetch_page, parse_page
from db.database import Database
import logging

# Logging configuration to keep track of errors & events from scraper's activities
# Paginated data handling repeatedly fetches pages until no data is found
def scrape_all_pages(base_url):
    page = 1
    data_collected = []
    while True:
        url = f"{base_url}&page={page}"
        html = fetch_page(url)
        if html:
            data = parse_page(html)
            if not data:
                logging.info(f"No data found on page {page}. Ending scrape.")
                break
            data_collected.extend(data)
            page += 1
        else:
            logging.info(f"Failed to retrieve page {page}. Ending scrape.")
            break
    return data_collected

def main():
    url_base = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9'
    # Adjust the URL as per actual page, but this one is for Morris County, NJ foreclosure auctions

    results = scrape_all_pages(url_base)
    db = Database('auctions.db')
    for result in results:
        db.insert_auction(result)
    db.close()
    logging.info("Scraping completed successfully.")

if __name__ == '__main__':
    main()

