import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
import sys
import os

# Import fungsi dari utils/extract.py
# Sesuaikan path berdasarkan struktur proyek
current_dir = os.path.dirname(os.path.abspath(__file__))  # folder tests
root_dir = os.path.dirname(current_dir)  # root project
sys.path.append(root_dir)

# Import dari module utils
from utils.extract import fetching_content, extract_product_data, scrape_product

class TestFetchingContent(unittest.TestCase):
    @patch('requests.Session')
    def test_fetching_content_success(self, mock_session):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body>Test Content</body></html>'
        
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_response
        
        # Call the function
        result = fetching_content('https://example.com')
        
        # Verify the result
        self.assertEqual(result, b'<html><body>Test Content</body></html>')
        session_instance.get.assert_called_once()
    
    @patch('requests.Session')
    def test_fetching_content_404(self, mock_session):
        # Setup mock response for 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_response
        
        # Call the function
        result = fetching_content('https://example.com/not-found')
        
        # Verify the result is None for 404
        self.assertIsNone(result)
    
    @patch('requests.Session')
    def test_fetching_content_exception(self, mock_session):
        # Setup mock to raise exception
        session_instance = mock_session.return_value
        session_instance.get.side_effect = requests.exceptions.RequestException("Connection error")
        
        # Call the function
        result = fetching_content('https://example.com/error')
        
        # Verify the result is None
        self.assertIsNone(result)


class TestExtractProductData(unittest.TestCase):
    def test_extract_complete_data(self):
        # Create sample HTML with all data
        html = '''
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$99.99</span>
            <p style="font-size: 14px; color: #777;">Rating: 4.5/5</p>
            <p style="font-size: 14px; color: #777;">Colors: Red, Blue</p>
            <p style="font-size: 14px; color: #777;">Size: M</p>
            <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        product_card = soup.find('div', class_='product-details')
        
        result = extract_product_data(product_card)
        
        # Assert all fields are correctly extracted
        self.assertEqual(result['Title'], 'Test Product')
        self.assertEqual(result['Price'], '$99.99')
        self.assertEqual(result['Rating'], '4.5/5')
        self.assertEqual(result['Colors'], 'Colors: Red, Blue')
        self.assertEqual(result['Size'], 'M')
        self.assertEqual(result['Gender'], 'Unisex')
    
    def test_extract_minimum_data(self):
        # Create sample HTML with minimum data
        html = '''
        <div class="product-details">
            <h3 class="product-title">Minimal Product</h3>
            <p class="price">$50.00</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        product_card = soup.find('div', class_='product-details')
        
        result = extract_product_data(product_card)
        
        # Assert required fields exist and optional ones are None
        self.assertEqual(result['Title'], 'Minimal Product')
        self.assertEqual(result['Price'], '$50.00')
        self.assertIsNone(result['Rating'])
        self.assertIsNone(result['Colors'])
        self.assertIsNone(result['Size'])
        self.assertIsNone(result['Gender'])
    
    def test_extract_no_title(self):
        # Test case when title is missing
        html = '''
        <div class="product-details">
            <span class="price">$75.00</span>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        product_card = soup.find('div', class_='product-details')
        
        result = extract_product_data(product_card)
        
        # Assert default title is used
        self.assertEqual(result['Title'], 'No title')
        self.assertEqual(result['Price'], '$75.00')
    
    def test_extract_no_price(self):
        # Test case when price is missing
        html = '''
        <div class="product-details">
            <h3 class="product-title">No Price Product</h3>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        product_card = soup.find('div', class_='product-details')
        
        result = extract_product_data(product_card)
        
        # Assert default price message is used
        self.assertEqual(result['Title'], 'No Price Product')
        self.assertEqual(result['Price'], 'Price Not Found')


class TestScrapeProduct(unittest.TestCase):
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_scrape_single_page(self, mock_sleep):
        with patch('utils.extract.fetching_content') as mock_fetching_content:
            # Create mock HTML for a single page with 2 products
            html_content = '''
            <html>
                <body>
                    <div class="product-details">
                        <h3 class="product-title">Product 1</h3>
                        <span class="price">$10.99</span>
                        <p style="font-size: 14px; color: #777;">Rating: 4.0/5</p>
                    </div>
                    <div class="product-details">
                        <h3 class="product-title">Product 2</h3>
                        <span class="price">$20.99</span>
                        <p style="font-size: 14px; color: #777;">Size: L</p>
                    </div>
                </body>
            </html>
            '''
            # Configure mock to return our HTML content
            mock_fetching_content.return_value = html_content
            
            # Call the function
            result = scrape_product(
                base_url="https://example.com/page/{}",
                first_page_url="https://example.com",
                start_page=1,
                delay=0  # No delay for testing
            )
            
            # Verify the results
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['Title'], 'Product 1')
            self.assertEqual(result[0]['Price'], '$10.99')
            self.assertEqual(result[0]['Rating'], '4.0/5')
            self.assertEqual(result[1]['Title'], 'Product 2')
            self.assertEqual(result[1]['Price'], '$20.99')
            self.assertEqual(result[1]['Size'], 'L')
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_scrape_multiple_pages(self, mock_sleep):
        with patch('utils.extract.fetching_content') as mock_fetching_content:
            # Create mock HTML for two pages with next button on first page
            html_page1 = '''
            <html>
                <body>
                    <div class="product-details">
                        <h3 class="product-title">Page 1 Product</h3>
                        <span class="price">$30.99</span>
                    </div>
                    <li class="next">Next Page</li>
                </body>
            </html>
            '''
            
            html_page2 = '''
            <html>
                <body>
                    <div class="product-details">
                        <h3 class="product-title">Page 2 Product</h3>
                        <span class="price">$40.99</span>
                    </div>
                    <!-- No next button on last page -->
                </body>
            </html>
            '''
            
            # Configure mock to return different HTML based on page number
            mock_fetching_content.side_effect = [html_page1, html_page2]
            
            # Call the function
            result = scrape_product(
                base_url="https://example.com/page/{}",
                first_page_url="https://example.com",
                start_page=1,
                delay=0  # No delay for testing
            )
            
            # Verify the results
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['Title'], 'Page 1 Product')
            self.assertEqual(result[1]['Title'], 'Page 2 Product')
            
            # Verify the URLs requested
            self.assertEqual(mock_fetching_content.call_count, 2)
    
    @patch('time.sleep')
    def test_scrape_page_not_found(self, mock_sleep):
        with patch('utils.extract.fetching_content') as mock_fetching_content:
            # Create mock HTML for a "Page not found" response
            html_error = '''
            <html>
                <body>
                    <h1>Page not found</h1>
                </body>
            </html>
            '''
            
            # Configure mock to return error page
            mock_fetching_content.return_value = html_error
            
            # Call the function
            result = scrape_product(
                base_url="https://example.com/page/{}",
                first_page_url="https://example.com/invalid",
                start_page=1,
                delay=0
            )
            
            # Verify the result is an empty list
            self.assertEqual(result, [])
    
    @patch('time.sleep')
    def test_scrape_no_products(self, mock_sleep):
        with patch('utils.extract.fetching_content') as mock_fetching_content:
            # Create mock HTML for a page with no products
            html_no_products = '''
            <html>
                <body>
                    <!-- No product-details divs -->
                </body>
            </html>
            '''
            
            # Configure mock to return page with no products
            mock_fetching_content.return_value = html_no_products
            
            # Call the function
            result = scrape_product(
                base_url="https://example.com/page/{}",
                first_page_url="https://example.com/empty",
                start_page=1,
                delay=0
            )
            
            # Verify the result is an empty list
            self.assertEqual(result, [])
    
    @patch('time.sleep')
    def test_scrape_content_none(self, mock_sleep):
        with patch('utils.extract.fetching_content') as mock_fetching_content:
            # Configure mock to return None (simulating connection error)
            mock_fetching_content.return_value = None
            
            # Call the function
            result = scrape_product(
                base_url="https://example.com/page/{}",
                first_page_url="https://example.com/error",
                start_page=1,
                delay=0
            )
            
            # Verify the result is an empty list
            self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
