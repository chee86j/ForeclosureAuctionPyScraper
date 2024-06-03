# Foreclosure Auctions Python Scraper

Welcome to the Foreclosure Auctions Python Scraper — a premier tool for
seamlessly gathering data from government foreclosure auctions sites.
Powered by Python, this robust scraper harnesses the capabilities of
the BeautifulSoup and Requests libraries to meticulously parse and
extract crucial auction data from websites, starting with our example
site at "https://salesweb.civilview.com/Sales/SalesSearch?countyId=9"
for Morris County, New Jersey.

My solution is designed for professionals in real estate, data analysis,
and investment sectors looking to access up-to-date and comprehensive
auction data without the hassle of manual research. Whether you're
monitoring auction trends or preparing investment strategies, this tool
provides the data backbone you need.

## Key Features

1.  Reliable Data Extraction: Automatically scrapes detailed auction data
    including case numbers, sale dates, property addresses, and status.
2.  Easy to Set Up and Use: Quick setup process and straightforward commands
    to get the data you need.
3.  Efficient Data Storage: Utilizes SQLite, a lightweight database solution,
    to store and manage the extracted data efficiently.
4.  Customizable and Expandable: Designed with modularity in mind, allowing
    for easy updates and customization to cater to specific user needs.

## Technologies & Libraries

1.  BeautifulSoup and Requests libraries to scrape HTML elements
2.  SQLite for data storage

## Installation

1.  Clone the repository
2.  Set up a virtual environment
    -MacOS/Linux: source venv/bin/activate
    -Windows: venv\Scripts\activate
3.  Install the required packages
    -pip install requests beautifulsoup4

## Running the Scraper

1.  Run the scraper
    -python src/main.py

## Testing the Scraper

1.  Run the tests
    -python -m unittest test/test_scraper.py
