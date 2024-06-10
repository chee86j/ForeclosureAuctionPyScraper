# Entry point for app to run the scraper and store the data in the database
# & paginated data
import asyncio
from scraper.scraper import parse_page
from db.database import Database
import logging

# Configure logging
logging.basicConfig(filename='main.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Paginate through the results and scrape each page
async def scrape_all_pages(base_url, session):
    page = 1
    data_collected = []
    while True:
        url = f"{base_url}&page={page}"
        page_data = await parse_page(session, url)
        if page_data:
            data_collected.extend(page_data)
            page += 1
        else:
            logging.info(f"No data found on page {page}. Ending scrape.")
            break
    return data_collected

async def main():
    url_base = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9'
        # Adjust the URL as per actual page, but this one is for Morris County, NJ foreclosure auctions

    async with aiohttp.ClientSession() as session:
        results = await scrape_all_pages(url_base, session)
        db = Database('auctions.db')
        for result in results:
            db.insert_auction(result)
        db.close()
    logging.info("Scraping completed successfully.")

if __name__ == '__main__':
    asyncio.run(main())

