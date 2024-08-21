# Implements tests case for the scraper module
import unittest
import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Path Adjusted to include the src directory where the scraper module is located
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from scraper.scraper import parse_page

class TestScraper(unittest.IsolatedAsyncioTestCase):
    async def test_parse_page(self):
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
                        <td><a href="/Sales/SaleDetails?PropertyId=12345">Details</a></td>
                    </tr>
                    <tr class="salesSearchResult" data-target="sale-details">
                        <td data-label="Case #">67890</td>
                        <td data-label="Sale Date">02/02/2024</td>
                        <td data-label="Property Address">456 Elm St</td>
                        <td data-label="Status">Pending</td>
                        <td><a href="/Sales/SaleDetails?PropertyId=67890">Details</a></td>
                    </tr>
                </table>
            </body>
        </html>
        '''
        # Using patch to mock asynchronous calls within your parse_page function
        with patch('scraper.scraper.fetch_page', MagicMock(return_value=html)):
            results = await parse_page(None, "http://fakeurl.com")
            self.assertEqual(len(results), 2)  # Expecting two entries
            self.assertIn('details_url', results[0])
            self.assertIn('details_url', results[1])
            self.assertEqual(results[0]['case_number'], '12345')
            self.assertEqual(results[1]['case_number'], '67890')

if __name__ == '__main__':
    unittest.main()