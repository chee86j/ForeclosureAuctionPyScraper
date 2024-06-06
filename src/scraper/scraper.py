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
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
    "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/73.0"
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
        case_number = clean_text(auction.find('td', {'data-label': 'Case #'}).text)
        sale_date = convert_date_format(clean_text(auction.find('td', {'data-label': 'Sale Date'}).text))
        property_address = clean_text(auction.find('td', {'data-label': 'Property Address'}).text)
        status = clean_text(auction.find('td', {'data-label': 'Status'}).text)
        details_link = soup.find('a', text='Details')['href']  # 'Details' is the link text
        details_url = f"https://salesweb.civilview.com{details_link}"

        data.append({
            'case_number': case_number,
            'sale_date': sale_date,
            'property_address': property_address,
            'status': status,
            'details_url': details_url
        })
    return data

def fetch_details(url):
    html = fetch_page(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        attorney_name = clean_text(soup.find('span', {'id': 'attorneyName'}).text)  # Example ID
        plaintiff_name = clean_text(soup.find('span', {'id': 'plaintiffName'}).text)  # Example ID
        return {
            'attorney_name': attorney_name,
            'plaintiff_name': plaintiff_name
        }
    else:
        return {}

def clean_text(text):
    """Strip whitespace and handle any other text cleanup."""
    return text.strip()

def convert_date_format(date_str):
    """Convert date string from 'MM/DD/YYYY' to 'YYYY-MM-DD' if needed."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        logging.error(f"Date conversion error for date: {date_str}")
        return date_str  # Return original if error occurs
