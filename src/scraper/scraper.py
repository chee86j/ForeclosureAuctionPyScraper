import requests
import time
import logging
from random import choice
from bs4 import BeautifulSoup

# Configure logging to keep track of errors and events from scraper's activities
logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# User-Agents Rotation to prevent blocking and masking to prevent detection to appear as a bot
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # Add more user agents as needed
]

def fetch_page(url):
    headers = {'User-Agent': choice(USER_AGENTS)}
    try:
        time.sleep(1)  # Sleep delay added to prevent flooding the server to prevent your IP from being blocked
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    auctions = soup.find_all('tr', {'data-target': 'sale-details'})
    data = []
    for auction in auctions:
        case_number = auction.find('td', {'data-label': 'Case #'}).text.strip()
        sale_date = auction.find('td', {'data-label': 'Sale Date'}).text.strip()
        property_address = auction.find('td', {'data-label': 'Property Address'}).text.strip()
        status = auction.find('td', {'data-label': 'Status'}).text.strip()
        data.append({
            'case_number': case_number,
            'sale_date': sale_date,
            'property_address': property_address,
            'status': status
        })
    return data
