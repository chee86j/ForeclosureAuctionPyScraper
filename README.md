# Foreclosure Auctions Python Scraper

Welcome to the Foreclosure Auctions Python Scraper — a premier tool for
seamlessly gathering data from government foreclosure auctions sites.
Powered by Python, this robust scraper leverages the capabilities of
Selenium, BeautifulSoup, and aiohttp libraries to meticulously parse and
extract crucial auction data from websites, starting with our example
site at "https://salesweb.civilview.com/Sales/SalesSearch?countyId=9"
for Morris County, New Jersey.

My solution is designed for professionals in real estate, data analysis,
and investment sectors looking to access up-to-date and comprehensive
auction data without the hassle of manual research. Whether you're
monitoring auction trends or preparing investment strategies, this tool
provides the data backbone you need.

---

## ----------QUICK START---------- (Note: Format and Content will need to be Adjusted for each Data Scraping Source Site)

0. Prerequisites:
   - Python 3.x installed on your system.
   - SQLite installed on your system.
   - Chrome browser installed on your system.
   - ChromeDriver downloaded and path set in the scraper.py file (Line 23)
   - Execute ChromeDriver
1. Clone the repository.
2. Set up a virtual environment:
   - MacOS/Linux: source venv/bin/activate
   - Windows: venv\Scripts\activate
3. Install required packages:
   - pip install selenium aiohttp beautifulsoup4 aiolimiter pandas python-dotenv requests
4. Run the scraper:
   - python src/main.py
5. Export the scraped data to CSV:
   - python export_to_csv.py

---

## Key Features

1.  **Reliable Data Extraction**: Automatically scrapes detailed auction data
    including case numbers, sale dates, property addresses, and status.
2.  **Efficient Pagination Handling**: Capable of navigating through multiple pages
    to collect all available listings.
3.  **Detailed Data Access**: Fetches additional details from each listing's
    'Details'
    page, extracting specific information like attorney and plaintiff names.
4.  **Advanced Web Scraping with Selenium**: Uses Selenium to handle complex web
    interactions and dynamic content loading, ensuring accurate data extraction even
    from JavaScript-heavy sites.
5.  **Easy to Set Up and Use**: Quick setup process and straightforward commands
    to get the data you need.
6.  **Efficient Data Storage**: Utilizes SQLite, a lightweight database solution,
    to store and manage the extracted data efficiently.
7.  **Export Data to CSV**: Easily export the scraped data from the SQLite database
    to a CSV file for further analysis or reporting.
8.  **Customizable and Expandable**: Designed with modularity in mind, allowing
    for easy updates and customization to cater to specific user needs.

## Technologies & Libraries

1.  Selenium for automating web browser interactions.
2.  BeautifulSoup for parsing HTML and XML documents.
3.  aiohttp for asynchronous HTTP requests.
4.  Asyncio for managing asynchronous I/O operations.
5.  AsyncLimiter for rate-limiting asynchronous operations.
6.  SQLite for storing and managing the extracted data.
7.  Python's logging module for error logging & debugging.
8.  Pandas for exporting data to CSV files.
9.  Python-dotenv for managing environment variables.
10. Requests for making HTTP requests.

## Prerequisites

Before running the scraper, ensure you have the following installed:

1. **Python**: Ensure Python 3.x is installed on your system. [python.org](https://www.python.org/downloads/).
2. **SQLite**: Make sure SQLite is installed on your system:

   - [SQLite Download page](https://sqlite.org/download.html) and follow the installation instructions.
     Look under'Precompiled Binaries for Windows' for the [DLL]
   - Verify installation by running sqlite3 in your terminal. If installed, you should see the SQLite version and a command-line interface.

3. **Chrome Browser**: The scraper uses Chrome as the default browser for Selenium.
   Ensure you have Chrome installed on your system.

4. **ChromeDriver**: Download the ChromeDriver that matches your Chrome version:

   - (https://googlechromelabs.github.io/chrome-for-testing/). Match with your OS
   - After downloading, extract the file and note the path to the chromedriver executable.
   - Make sure the chromedriver file has executable permissions (on macOS/Linux, run chmod +x /path/to/chromedriver).

5. Clone the repository.
6. Set up a virtual environment:
   - MacOS/Linux: source venv/bin/activate
   - Windows: venv\Scripts\activate
7. Install required packages:
   - pip install selenium aiohttp beautifulsoup4 aiolimiter pandas python-dotenv requests

## Running the Scraper within the Virtual Environment

bash
python src/main.py

## Exporting Scraped Data to CSV (Only After Running the Scraper)

bash
python export_to_csv.py

## Testing the Scraper

1.  Run the tests
    -python -m unittest test/test_scraper.py

## Customizing the Scraper for a Different Website

If you want to scrape data from a different website, you'll need to make adjustments to the following components of the scraper:

1. HTML Structure & Parsing (`src/scraper/scraper.py`)

   - Understand the Target Website's HTML Structure: Inspect the HTML structure of the new target site using your browser's Developer Tools (usually accessible via F12 or right-clicking and selecting "Inspect").
   - Update Selectors: Modify the `fetch_page_selenium` and `parse_page_selenium` functions to correctly select and extract data based on the new site's HTML structure.
     For example, if the table or data fields you need have different class or id attributes, update the BeautifulSoup selectors accordingly.
   - Handle Pagination: Ensure that the pagination handling logic is compatible with the new site. You may need to update how the scraper navigates through multiple pages if the structure differs.

2. Database Schema (`src/db/database.py`)

   - Adjust the Table Schema: If the data structure or fields you are scraping differ, update the `create_table` function to reflect the new schema.
   - Insert Logic: Modify the `insert_data` function to correctly map the scraped data to the database columns. Ensure that the field names in your database match those in your scraping code.

3. Main Script (`src/main.py`)

   - Additional Data Fields: If you need to store additional data fields from the new site, add them to the database schema and update the insert logic accordingly.
   - Adjust the URL: Update the `url` variable in `main.py` to point to the new site.
   - Function Calls: Ensure that the functions you call in `main` are correctly adapted to handle the new site's structure and data requirements.
   - Logging and Error Handling: Optionally, update any logging messages to reflect the new data and context of the scraping task.

4. Testing
   - Update or Create New Tests: Modify existing tests in the test/ directory or create new ones to cover the changes you've made for the new site. This ensures that your scraper works as expected on the new target site.

## Troubleshooting

ChromeDriver Issues: Ensure that the path to chromedriver is correctly set in your `scraper.py`. If you encounter issues with Selenium not finding chromedriver, make sure you have the correct version and that it is executable.

Database Issues: If you experience issues with SQLite, ensure that your database path is correctly set and that you have the necessary permissions to write to it.
