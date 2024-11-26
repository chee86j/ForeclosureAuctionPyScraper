from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def fetch_page_selenium_headless(url):
    """Fetch page content using Selenium in headless mode."""
    try:
        options = Options()
        options.headless = True
        # service = Service(executable_path='/Users/jchee/Downloads/chromedriver-mac-x64/chromedriver')
        service = Service(executable_path='C:\\chromedriver-win64\\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        logging.error(f"Error fetching {url} with Selenium headless: {e}")
        return None

def parse_zillow_page(url):
    html = fetch_page_selenium_headless(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        return {
            'url': url,
            'zillow_details': parse_zillow_details(soup),
            'tax_history': parse_tax_history(soup),
            'property_details': parse_property_details(soup)
        }
    else:
        logging.error("No HTML content returned")
        return {}

def export_data_to_csv(data, csv_file):
    """Export parsed data to a CSV file."""
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        logging.info(f"Data exported to {csv_file} successfully.")
    except Exception as e:
        logging.error(f"Error exporting data to {csv_file}: {e}")

def parse_zillow_details(soup):
    details = {}
    
    # Extracting Zestimate
    zestimate_span = soup.find('span', {'data-testid': 'zestimate-text'})
    details['zestimate'] = zestimate_span.find('span').get_text(strip=True) if zestimate_span else "Not available"
    # Extracting bed, bath, and sqft
    bed_bath_sqft = soup.find('span', {'data-testid': 'bed-bath-beyond'})
    details['bed_bath_sqft'] = bed_bath_sqft.get_text(strip=True) if bed_bath_sqft else "Not available"
    return details

def parse_tax_history(soup):
    tax_history = []
    tax_table = soup.find('table', attrs={'aria-label': "Table of tax history"})
    if tax_table:
        rows = tax_table.find('tbody').find_all('tr')
        for row in rows:
            year = row.find('th').get_text(strip=True)
            property_taxes = row.find_all('td')[0].get_text(strip=True)
            tax_assessment = row.find_all('td')[1].get_text(strip=True)
            tax_history.append({
                'year': year,
                'property_taxes': property_taxes,
                'tax_assessment': tax_assessment
            })
    return tax_history

def parse_property_details(soup):
    property_type_span = soup.find('span', string="Type:")
    property_type = property_type_span.find_next('span').get_text(strip=True) if property_type_span else "Not available"
    return {'property_type': property_type}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        urls = sys.argv[1:]  # Taking multiple URLs from command-line arguments
        results = []
        for url in urls:
            try:
                data = parse_zillow_page(url)
                if data:
                    results.append(data)
                    logging.info(f"Successfully parsed data for {url}")
                else:
                    logging.warning(f"No data returned for {url}")
            except Exception as e:
                logging.error(f"Failed to process {url} with error {e}")
        if results:
            export_data_to_csv(results, 'exported_zillow_data.csv')
        else:
            logging.warning("No data to export.")
    else:
        logging.error("No URLs provided. Usage: python zillow_scraper.py <url1> <url2> ...")
        sys.exit("Usage: python zillow_scraper.py <url1> <url2> ...")

#   Run this script: `python src/zillow_scraper.py ZillowURL`