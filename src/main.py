# Entry point for app to run the scraper and store the data in the database
# & paginated data
from scraper.scraper import fetch_page, parse_page
from db.database import Database

def main():
    url_base = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9' 
    # Adjust the URL as per actual page, but this one is for Morris County, NJ foreclosure auctions
    html_content = fetch_page(url_base)
    if html_content:
        auction_data = parse_page(html_content)
        db = Database('auctions.db')
        for auction in auction_data:
            db.insert_auction(auction)
        db.close()

if __name__ == '__main__':
    main()
