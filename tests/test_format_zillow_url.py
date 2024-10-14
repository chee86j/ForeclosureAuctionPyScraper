# test_format_zillow_url.py

import unittest
import pandas as pd
import os
from format_zillow_url import format_zillow_url, export_to_csv

class TestZillowUrlFormatter(unittest.TestCase):

    def test_format_zillow_url(self):
        # Test with a simple address
        address = "123 Main St, Anytown, USA"
        expected_url = "https://www.zillow.com/homes/123-Main-St-Anytown-USA_rb/"
        result = format_zillow_url(address)
        self.assertEqual(result, expected_url)

        # Test with no spaces and commas
        address = "456ElmStreet"
        expected_url = "https://www.zillow.com/homes/456ElmStreet_rb/"
        result = format_zillow_url(address)
        self.assertEqual(result, expected_url)

        # Test with special characters (which should be handled)
        address = "789 Main St!@#, Anytown"
        expected_url = "https://www.zillow.com/homes/789-Main-St!@#-Anytown_rb/"
        result = format_zillow_url(address)
        self.assertEqual(result, expected_url)

    def test_export_to_csv(self):
        # Create sample data
        data = [
            {"address": "123 Main St, Anytown, USA", "Zillow URL": "https://www.zillow.com/homes/123-Main-St-Anytown-USA_rb/"},
            {"address": "456 Elm St, AnotherTown, USA", "Zillow URL": "https://www.zillow.com/homes/456-Elm-St-AnotherTown-USA_rb/"}
        ]
        
        # Export to CSV
        filename = "test_export.csv"
        export_to_csv(data, filename)

        # Read back the CSV to verify it
        df = pd.read_csv(filename)
        self.assertEqual(len(df), 2)
        self.assertEqual(df["address"].iloc[0], "123 Main St, Anytown, USA")
        self.assertEqual(df["Zillow URL"].iloc[1], "https://www.zillow.com/homes/456-Elm-St-AnotherTown-USA_rb/")

        # Clean up
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
