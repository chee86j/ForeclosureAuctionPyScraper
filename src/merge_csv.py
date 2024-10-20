import pandas as pd
import logging
import sys

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def merge_csv_files(address_file, zillow_url_file, output_file='merged_data.csv'):
    try:
        # Load the CSV files
        address_data = pd.read_csv(address_file)
        zillow_data = pd.read_csv(zillow_url_file)

        # Merge the data on the 'address' column
        merged_data = pd.merge(address_data, zillow_data, on='address', how='left')

        # Export the merged data to a new CSV file
        merged_data.to_csv(output_file, index=False)
        logging.info(f"Merged data exported to {output_file} successfully.")
        print(f"Merged data has been exported to {output_file}")

    except Exception as e:
        logging.error(f"Failed to merge files: {e}")
        sys.exit(f"Failed to merge files: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        address_file = sys.argv[1]
        zillow_url_file = sys.argv[2]
        
        # Merge the CSV files
        merge_csv_files(address_file, zillow_url_file)
    else:
        logging.error("Usage: python script.py <address_file> <zillow_url_file>")
        sys.exit("Usage: python script.py <address_file> <zillow_url_file>")
