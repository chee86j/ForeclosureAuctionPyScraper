from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def fetch_page_selenium_headless(url):
    """Fetch page content using Selenium in headless mode."""
    try:
        options = Options()
        options.headless = True
        service = Service(executable_path='/Users/jchee/Downloads/chromedriver-mac-x64/chromedriver')
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
            'zillow_details': parse_zillow_details(soup),
            'tax_history': parse_tax_history(soup),
            'property_details': parse_property_details(soup)
        }
    else:
        logging.error("No HTML content returned")
        return {}

def parse_zillow_details(soup):
    details = {}
    zestimate_text = soup.find('span', {'data-testid': 'zestimate-text'})
    rent_zestimate = zestimate_text.get_text(strip=True) if zestimate_text else "Not available"
    bed_bath_sqft = soup.find('span', {'data-testid': 'bed-bath-beyond'})
    bed_bath_sqft_text = bed_bath_sqft.get_text(strip=True) if bed_bath_sqft else "Not available"
    details['rent_zestimate'] = rent_zestimate
    details['bed_bath_sqft'] = bed_bath_sqft_text
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
    details = {}
    detail_div = soup.find('div', class_='hdp__sc-1j01zad-0 hGwlRq')
    if detail_div:
        lot_size = detail_div.find('span', text="Lot:").find_next('span').get_text(strip=True)
        property_type = detail_div.find('span', text="Type:").find_next('span').get_text(strip=True)
        details['lot_size'] = lot_size
        details['property_type'] = property_type
    return details

# Example usage
if __name__ == "__main__":
    url = "https://www.zillow.com/homes/21-Crimson-Lane-Mine-Hill-NJ-07803_rb/"
    data = parse_zillow_page(url)
    print(data)
