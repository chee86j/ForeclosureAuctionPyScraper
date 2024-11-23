from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
import pandas as pd
import time

# Configure logging
logging.basicConfig(
    filename='morris_scraper.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def extract_primary_name(defendant):
    """Extract the primary name before the ';' and format it as 'Last, First Middle'."""
    try:
        # Extract name before ';'
        primary_name = defendant.split(";")[0].strip()
        names = primary_name.split(" ")

        # Check for valid name structure
        if len(names) >= 2:
            last_name = names[-1]  # Last word is the last name
            first_name = names[0]  # First word is the first name
            middle_names = " ".join(names[1:-1])  # Everything in between
            return f"{last_name}, {first_name} {middle_names}".strip()
        return primary_name
    except Exception as e:
        logging.error(f"Error extracting primary name: {e}")
        return defendant.strip()

def fetch_page_selenium(search_query):
    """Fetch the search results page using Selenium."""
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    
    # Update the path to your ChromeDriver
    service = Service(executable_path='/Users/jchee/Downloads/chromedriver-mac-x64/chromedriver')  # Update this path as needed

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the website
        url = "https://mcclerksng.co.morris.nj.us/publicsearch/"
        driver.get(url)
        logging.info(f"Opened URL: {url}")
        time.sleep(3)  # Wait for the page to load

        # Locate the search bar and enter the defendant's name
        search_box = driver.find_element(By.CSS_SELECTOR, "input[name='partyName']")  # Match provided selector
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        logging.info(f"Performed search with query: {search_query}")
        time.sleep(5)  # Wait for search results to load

        # Return the page source
        return driver.page_source

    except Exception as e:
        logging.error(f"Error fetching page for query '{search_query}': {e}")
        return None
    finally:
        driver.quit()

def parse_table(html):
    """Parse the HTML and extract table data."""
    data = []
    try:
        soup = BeautifulSoup(html, "html.parser")
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
        logging.info(f"Extracted {len(data)} rows from the table.")
    except Exception as e:
        logging.error(f"Error parsing table: {e}")
    return data

def export_to_csv(data, filename):
    """Export the scraped data to a CSV file."""
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logging.info(f"Data exported to {filename} successfully.")
        print(f"Data has been exported to {filename}")
    except Exception as e:
        logging.error(f"Error exporting data to {filename}: {e}")
        print(f"Failed to export data to {filename}")

def retry_prompt(defendant):
    """Prompt the user for a revised input name."""
    revised_input = input(f"No data found for '{defendant}'. Please type the revised input name manually now: ").strip()
    return revised_input

def main():
    """Main function to run the scraper."""
    # Load merged_data.csv
    try:
        merged_data = pd.read_csv("merged_data.csv")
    except Exception as e:
        logging.error(f"Failed to load merged_data.csv: {e}")
        print("Failed to load merged_data.csv.")
        return

    # Iterate through defendants and search for each
    for _, row in merged_data.iterrows():
        defendant = row['defendant']
        search_query = extract_primary_name(defendant)

        while True:
            logging.info(f"Starting search for defendant: {search_query}")
            print(f"Searching for: {search_query}")

            # Fetch the page HTML
            html = fetch_page_selenium(search_query)
            if html:
                # Parse the table data
                data = parse_table(html)

                if data:
                    # Export the data to CSV
                    output_filename = f"morris_clerk_data_{search_query.replace(' ', '_').replace(',', '')}.csv"
                    export_to_csv(data, output_filename)
                    break
                else:
                    logging.warning(f"No data scraped for: {search_query}")
                    print(f"No data found for: {search_query}")
                    search_query = retry_prompt(defendant)
            else:
                logging.error(f"Failed to fetch the page for: {search_query}")
                print(f"Failed to fetch the page for: {search_query}")
                search_query = retry_prompt(defendant)

if __name__ == "__main__":
    main()
