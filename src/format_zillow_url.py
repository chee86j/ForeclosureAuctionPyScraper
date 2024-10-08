import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def format_zillow_url(address):
    """Convert the address to a Zillow URL format."""
    try:
        formatted_address = address.replace(" ", "-").replace(",", "")
        zillow_url = f"https://www.zillow.com/homes/{formatted_address}_rb/"
        return zillow_url
    except Exception as e:
        logging.error(f"Error formatting Zillow URL for {address}: {e}")
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
            # Load addresses from CSV file
            data = pd.read_csv(address_file)
            addresses = data['address'].tolist()
            
            results = []
            for address in addresses:
                zillow_url = format_zillow_url(address)
                if zillow_url:
                    results.append({'address': address, 'Zillow URL': zillow_url})
                    logging.info(f"Successfully formatted URL for {address}")
                else:
                    logging.warning(f"Failed to format URL for {address}")

            # Export results to CSV
            export_to_csv(results)
            
        except Exception as e:
            logging.error(f"Failed to process file {address_file}: {e}")
            sys.exit(f"Failed to process file {address_file}: {e}")
    else:
        logging.error("Usage: python script.py <address_file>")
        sys.exit("Usage: python script.py <address_file>")