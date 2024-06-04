# Implements tests case for the scraper module
import unittest
import sys
import os

# Path Adjusted to include the src directory where the scraper module is located
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from scraper.scraper import parse_page

class TestScraper(unittest.TestCase):
    def test_parse_page(self):
        # Example HTML snippet mimicking structure of the auction listing page for testing
        html = '''
        <html>
            <body>
                <table>
                    <tr class="salesSearchResult" data-target="sale-details">
                        <td data-label="Case #">12345</td>
                        <td data-label="Sale Date">01/01/2024</td>
                        <td data-label="Property Address">123 Main St</td>
                        <td data-label="Status">Active</td>
                    </tr>
                    <tr class="salesSearchResult" data-target="sale-details">
                        <td data-label="Case #">67890</td>
                        <td data-label="Sale Date">02/02/2024</td>
                        <td data-label="Property Address">456 Elm St</td>
                        <td data-label="Status">Pending</td>
                    </tr>
                </table>
            </body>
        </html>
        '''
        results = parse_page(html)
        print("Parsed Results:", results)  # Debug: print the results
        self.assertEqual(len(results), 2)  # Expecting two entries
        self.assertEqual(results[0]['case_number'], '12345')
        self.assertEqual(results[0]['sale_date'], '01/01/2024')
        self.assertEqual(results[0]['property_address'], '123 Main St')
        self.assertEqual(results[0]['status'], 'Active')
        self.assertEqual(results[1]['case_number'], '67890')
        self.assertEqual(results[1]['sale_date'], '02/02/2024')
        self.assertEqual(results[1]['property_address'], '456 Elm St')
        self.assertEqual(results[1]['status'], 'Pending')

if __name__ == '__main__':
    unittest.main()
