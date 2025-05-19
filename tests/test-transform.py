import unittest
import pandas as pd
import numpy as np
from utils.transform import transform_data, transform_to_DataFrame, DIRTY_PATTERNS


class TestTransform(unittest.TestCase):

    def test_transform_data_valid_inputs(self):
        """Test transform_data with valid input values"""
        test_data = [
            {
                "Title": "Nike Running Shoes",
                "Price": "$120.50",
                "Rating": "4.5 / 5",
                "Colors": "3 colors",
                "Size": "Medium",
                "Gender": "Men"
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertEqual(result[0]["Title"], "Nike Running Shoes")
        self.assertEqual(result[0]["Price"], 120.50 * 16000)
        self.assertEqual(result[0]["Rating"], 4.5)
        self.assertEqual(result[0]["Colors"], 3)
        self.assertEqual(result[0]["Size"], "Medium")
        self.assertEqual(result[0]["Gender"], "Men")

    def test_transform_data_missing_values(self):
        """Test transform_data with missing values"""
        test_data = [
            {
                "Title": "Adidas T-shirt",
                "Price": None,
                "Rating": None,
                "Colors": None,
                "Size": "Large",
                "Gender": "Women"
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertEqual(result[0]["Title"], "Adidas T-shirt")
        self.assertIsNone(result[0]["Price"])
        self.assertIsNone(result[0]["Rating"])
        self.assertIsNone(result[0]["Colors"])
        self.assertEqual(result[0]["Size"], "Large")
        self.assertEqual(result[0]["Gender"], "Women")

    def test_transform_data_dirty_patterns(self):
        """Test transform_data with dirty pattern values"""
        test_data = [
            {
                "Title": "Unknown Product",
                "Price": "Price Unavailable",
                "Rating": "Not Rated",
                "Colors": "Unknown",
                "Size": "Small",
                "Gender": "Unisex"
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertIsNone(result[0]["Title"])
        self.assertIsNone(result[0]["Price"])
        self.assertIsNone(result[0]["Rating"])
        self.assertIsNone(result[0]["Colors"])
        self.assertEqual(result[0]["Size"], "Small")
        self.assertEqual(result[0]["Gender"], "Unisex")

    def test_transform_data_edge_cases(self):
        """Test transform_data with edge cases"""
        test_data = [
            {
                "Title": "Puma Jacket",
                "Price": "$0.00",
                "Rating": "0.0 / 5",
                "Colors": "0 colors",
                "Size": "",
                "Gender": None
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertEqual(result[0]["Title"], "Puma Jacket")
        self.assertEqual(result[0]["Price"], 0.0)
        self.assertEqual(result[0]["Rating"], 0.0)
        self.assertEqual(result[0]["Colors"], 0)
        self.assertEqual(result[0]["Size"], "")
        self.assertIsNone(result[0]["Gender"])

    def test_transform_data_invalid_formats(self):
        """Test transform_data with invalid format values"""
        test_data = [
            {
                "Title": "Reebok Shorts",
                "Price": "USD 75",  # Invalid price format
                "Rating": "Good",   # Invalid rating format
                "Colors": "Multiple",  # Invalid colors format
                "Size": "XL",
                "Gender": "Men"
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertEqual(result[0]["Title"], "Reebok Shorts")
        self.assertIsNone(result[0]["Price"])
        self.assertIsNone(result[0]["Rating"])
        self.assertIsNone(result[0]["Colors"])
        self.assertEqual(result[0]["Size"], "XL")
        self.assertEqual(result[0]["Gender"], "Men")

    def test_transform_data_multiple_items(self):
        """Test transform_data with multiple items"""
        test_data = [
            {
                "Title": "Nike Running Shoes",
                "Price": "$120.50",
                "Rating": "4.5 / 5",
                "Colors": "3 colors",
                "Size": "Medium",
                "Gender": "Men"
            },
            {
                "Title": "Unknown Product",
                "Price": "$85.75",
                "Rating": "3.8 / 5",
                "Colors": "2 colors",
                "Size": "Small",
                "Gender": "Women"
            }
        ]
        
        result = transform_data(test_data)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["Title"], "Nike Running Shoes")
        self.assertIsNone(result[1]["Title"])
        self.assertEqual(result[1]["Price"], 85.75 * 16000)

    def test_transform_to_DataFrame(self):
        """Test transform_to_DataFrame function"""
        test_data = [
            {
                "Title": "Nike Running Shoes",
                "Price": "$120.50",
                "Rating": "4.5 / 5",
                "Colors": "3 colors",
                "Size": "Medium",
                "Gender": "Men"
            },
            {
                "Title": "Adidas T-shirt",
                "Price": "$45.99",
                "Rating": "4.0 / 5",
                "Colors": "5 colors",
                "Size": "Large",
                "Gender": "Women"
            }
        ]
        
        df = transform_to_DataFrame(test_data)
        
        # Check DataFrame properties
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ["Title", "Price", "Rating", "Colors", "Size", "Gender"])
        
        # Check values
        self.assertEqual(df.iloc[0]["Title"], "Nike Running Shoes")
        self.assertEqual(df.iloc[0]["Price"], 120.50 * 16000)
        self.assertEqual(df.iloc[0]["Rating"], 4.5)
        self.assertEqual(df.iloc[0]["Colors"], 3)
        
        self.assertEqual(df.iloc[1]["Title"], "Adidas T-shirt")
        self.assertEqual(df.iloc[1]["Price"], 45.99 * 16000)
        self.assertEqual(df.iloc[1]["Rating"], 4.0)
        self.assertEqual(df.iloc[1]["Colors"], 5)

    def test_DIRTY_PATTERNS(self):
        """Test DIRTY_PATTERNS constant"""
        self.assertIn("Unknown Product", DIRTY_PATTERNS["Title"])
        self.assertIn("No title", DIRTY_PATTERNS["Title"])
        self.assertIn("Invalid Rating / 5", DIRTY_PATTERNS["Rating"])
        self.assertIn("Not Rated", DIRTY_PATTERNS["Rating"])
        self.assertIn(None, DIRTY_PATTERNS["Rating"])
        self.assertIn("Price Unavailable", DIRTY_PATTERNS["Price"])
        self.assertIn("Price Not Found", DIRTY_PATTERNS["Price"])
        self.assertIn(None, DIRTY_PATTERNS["Price"])


if __name__ == "__main__":
    unittest.main()