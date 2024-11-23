from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_table_data(driver):
    """Scrapes table data from the page."""
    data = []
    try:
        # Wait for the table to load
        time.sleep(5)
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.find_all("div", class_="ag-row")
        
        for row in rows:
            row_data = {}
            cells = row.find_all("div", class_="ag-cell")
            for cell in cells:
                colid = cell.get("colid")  # Extract colid
                value = cell.text.strip()  # Extract cell text
                if colid:
                    row_data[colid] = value
            if row_data:
                data.append(row_data)
    except Exception as e:
        print(f"Error while scraping table: {e}")
    return data

def main():
    # Set up ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU
    chrome_options.add_argument("--no-sandbox")
    
    # Update the path to your ChromeDriver
    service = Service(executable_path="/path/to/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the website
        driver.get("https://mcclerksng.co.morris.nj.us/publicsearch/")
        time.sleep(3)  # Wait for the page to load
        
        # Locate the search bar and enter the defendant's name
        search_box = driver.find_element(By.CSS_SELECTOR, "input[name='searchInput']")  # Update selector if necessary
        search_query = "ALLAMAN GLORIA M"  # Replace with desired name
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        time.sleep(5)
        
        # Scrape the table data
        data = scrape_table_data(driver)
        
        # Export to CSV
        if data:
            df = pd.DataFrame(data)
            df.to_csv("morris_clerk_data.csv", index=False)
            print("Data has been successfully exported to morris_clerk_data.csv")
        else:
            print("No data found or scraped.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
