
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

# Configure logging
logging.basicConfig(filename='morris_scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def fetch_morris_data(last_name, first_name):
    """Fetch data from the Morris County site for a given defendant."""
    url = "https://mcclerksng.co.morris.nj.us/publicsearch/"
    options = Options()
    options.headless = True
    service = Service(executable_path='/Users/jchee/Downloads/chromedriver-mac-x64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Find the search bar and enter the defendant's name
        search_bar = driver.find_element(By.ID, 'searchBar')  # Update the ID if necessary
        search_bar.send_keys(f"{last_name}, {first_name}")
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for the search results to load

        # Parse the page content
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('div', class_='ag-row')

        data = []
        for row in rows:
            row_data = {}
            cells = row.find_all('div', class_='ag-cell')
            for cell in cells:
                colid = cell.get('colid')
                if colid:
                    row_data[colid] = cell.get_text(strip=True)
            data.append(row_data)
        
        return data

    except Exception as e:
        logging.error(f"Error fetching data for {last_name}, {first_name}: {e}")
        return []

    finally:
        driver.quit()

def export_data_to_csv(data, csv_file):
    """Export scraped data to a CSV file."""
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        logging.info(f"Data exported to {csv_file} successfully.")
    except Exception as e:
        logging.error(f"Error exporting data to {csv_file}: {e}")

if __name__ == "__main__":
    last_name = input("Enter the defendant's last name: ").strip()
    first_name = input("Enter the defendant's first name: ").strip()
    
    data = fetch_morris_data(last_name, first_name)
    if data:
        csv_file = f"{last_name}_{first_name}_morris_data.csv"
        export_data_to_csv(data, csv_file)
        print(f"Data has been successfully exported to {csv_file}")
    else:
        print("No data found.")