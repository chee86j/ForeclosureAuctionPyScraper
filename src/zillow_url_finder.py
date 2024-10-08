import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sys
from googlesearch import search
import time

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def find_zillow_url(query):
    """Use Google search to find the Zillow URL for an address."""
    try:
        time.sleep(30)  # Delay each request to avoid hitting Google's rate limits
        for url in search(f"{query} site:zillow.com", num_results=1):
            return url
    except Exception as e:
        logging.error(f"Error during Google search for {query}: {e}")
        return None

def export_to_csv(data, filename='exported_zillow_urls.csv'):
    """Export data to CSV."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    logging.info(f"Data exported to {filename} successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        address_file = sys.argv[1]
        try:
            data = pd.read_csv(address_file)
            data['Zillow URL'] = data['address'].apply(find_zillow_url)
            export_to_csv(data)
        except Exception as e:
            logging.error(f"Failed to process file {address_file}: {e}")
            sys.exit(f"Failed to process file {address_file}: {e}")
    else:
        logging.error("Usage: python script.py <address_file>")
        sys.exit("Usage: python script.py <address_file>")
