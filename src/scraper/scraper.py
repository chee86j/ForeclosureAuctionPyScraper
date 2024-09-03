from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def fetch_page_selenium(url):
    """Fetch page content using Selenium."""
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    
    # Replace '/path/to/chromedriver' with the actual path to your ChromeDriver
    service = Service(executable_path='/Users/jchee/Downloads/chromedriver-mac-x64/chromedriver')  # Update this path

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to fully load

        html_content = driver.page_source
        logging.debug(f"Fetched HTML for {url}: {html_content[:5000]}")  # Log first 5000 characters of HTML
        return html_content

    except Exception as e:
        logging.error(f"Error fetching {url} with Selenium: {e}")
        return None

    finally:
        driver.quit()

def parse_page_selenium(url):
    """Parse page using Selenium."""
    html = fetch_page_selenium(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='table table-striped')
        if not table:
            logging.error(f"Failed to find the table on the page at URL: {url}")
            return []

        data = []
        rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
        for row in rows:
            cells = row.find_all('td')
            row_data = {
                'detail_link': f"https://salesweb.civilview.com{cells[0].find('a')['href']}" if cells[0].find('a') else 'No link provided',
                'sheriff_number': cells[1].text.strip() if len(cells) > 1 else None,
                'status_date': convert_date_format(cells[2].text.strip()) if len(cells) > 2 else None,
                'plaintiff': cells[3].text.strip() if len(cells) > 3 else None,
                'defendant': cells[4].text.strip() if len(cells) > 4 else None,
                'address': cells[5].text.strip() if len(cells) > 5 else None,
                'price': int(cells[6].text.strip().replace('$', '').replace(',', '')) if len(cells) > 6 else 0
            }
            data.append(row_data)
        
        return data
    else:
        logging.error("No HTML content returned")
        return []

def convert_date_format(date_str):
    """Convert date string from 'MM/DD/YYYY' to 'YYYY-MM-DD' if needed."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        logging.error(f"Date conversion error for date: {date_str}")
        return date_str  # Return original if error occurs
