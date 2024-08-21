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

1.  **Reliable Data Extraction**: Automatically scrapes detailed auction data
    including case numbers, sale dates, property addresses, and status.
2.  **Efficient Pagination Handling**: Capable of navigating through multiple pages to
    collect all available listings.
3.  **Detailed Data Access**: Fetches additional details from each listing's 'Details'
    page, extracting specific information like attorney and plaintiff names.
4.  **Easy to Set Up and Use**: Quick setup process and straightforward commands
    to get the data you need.
5.  **Efficient Data Storage**: Utilizes SQLite, a lightweight database solution,
    to store and manage the extracted data efficiently.
6.  **Customizable and Expandable**: Designed with modularity in mind, allowing
    for easy updates and customization to cater to specific user needs.

## Technologies & Libraries

1. `BeautifulSoup` for parsing HTML.
2. `aiohttp` for asynchronous web requests.
3. `Asyncio` for managing asynchronous tasks.
4. `AsyncLimiter` for rate limiting asynchronous requests.
5. `SQLite` for data storage.
6. Python's `logging` module for error logging and debugging.

## Prerequisites

Before running the scraper, ensure you have the following installed:

1. **Python**: Ensure Python 3.x is installed on your system. [python.org](https://www.python.org/downloads/).
2. **SQLite**: Make sure SQLite is installed on your system:

   - [SQLite Download page](https://sqlite.org/download.html) and follow the installation instructions.
     Look under'Precompiled Binaries for Windows' for the [DLL]
   - Verify installation by running `sqlite3` in your terminal. If installed, you should see the SQLite version and a command-line interface.

3. Clone the repository.
4. Set up a virtual environment:
   - MacOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
5. Install required packages:
   - `pip install aiohttp beautifulsoup4 aiolimiter`

## Running the Scraper

```bash
python src/main.py

## Testing the Scraper

1.  Run the tests
    -python -m unittest test/test_scraper.py
```
