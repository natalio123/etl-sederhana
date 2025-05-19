import unittest
import sys
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path so we can import the transform module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.transform import transform_data, transform_to_DataFrame, clean_existing_dataframe, DIRTY_PATTERNS

class TestTransform(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = [
            {
                "Title": "T-shirt",
                "Price": "$25.99",
                "Rating": "4.5/5",
                "Colors": "3 colors",
                "Size": "M",
                "Gender": "Men"
            },
            {
                "Title": "Hoodie",
                "Price": "$49.99",
                "Rating": "4.8/5",
                "Colors": "5 colors",
                "Size": "L",
                "Gender": "Unisex"
            },
            {
                "Title": "Unknown Product",  # Invalid title
                "Price": "$35.50",
                "Rating": "3.9/5",
                "Colors": "2 colors",
                "Size": "XL",
                "Gender": "Women"
            },
            {
                "Title": "Pants",
                "Price": "Price Unavailable",  # Invalid price
                "Rating": "4.2/5",
                "Colors": "4 colors",
                "Size": "M",
                "Gender": "Men"
            },
            {
                "Title": "Jacket",
                "Price": "$42.75",
                "Rating": "Not Rated",  # Invalid rating
                "Colors": "3 colors",
                "Size": "S",
                "Gender": "Women"
            },
            {
                "Title": "",  # Empty title
                "Price": "$15.99",
                "Rating": "3.6/5",
                "Colors": "2 colors", 
                "Size": "M",
                "Gender": "Unisex"
            }
        ]

    def test_transform_data(self):
        """Test the transform_data function correctly transforms data"""
        transformed = transform_data(self.sample_data)
        
        # Should only have valid entries (3 entries should be filtered out)
        self.assertEqual(len(transformed), 3)
        
        # Check first valid entry
        self.assertEqual(transformed[0]["Title"], "T-shirt")
        self.assertEqual(transformed[0]["Price"], 25.99 * 16000)
        self.assertEqual(transformed[0]["Rating"], 4.5)
        self.assertEqual(transformed[0]["Colors"], 3)
        self.assertEqual(transformed[0]["Size"], "M")
        self.assertEqual(transformed[0]["Gender"], "Men")
        
        # Check second valid entry
        self.assertEqual(transformed[1]["Title"], "Hoodie")
        self.assertEqual(transformed[1]["Price"], 49.99 * 16000)
        self.assertEqual(transformed[1]["Rating"], 4.8)
        self.assertEqual(transformed[1]["Colors"], 5)
        
        # Verify invalid entries are filtered out
        titles = [product["Title"] for product in transformed]
        self.assertNotIn("Unknown Product", titles)
        self.assertNotIn("", titles)
        
        # Check that all prices are valid (no None or NaN)
        for product in transformed:
            self.assertIsNotNone(product["Price"])
            self.assertFalse(pd.isna(product["Price"]))

    def test_transform_to_DataFrame(self):
        """Test the transform_to_DataFrame function creates a valid DataFrame"""
        df = transform_to_DataFrame(self.sample_data)
        
        # Check DataFrame properties
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 3)  # Only 3 valid entries should remain
        self.assertIn("Title", df.columns)
        self.assertIn("Price", df.columns)
        self.assertIn("Rating", df.columns)
        self.assertIn("Colors", df.columns)
        self.assertIn("Size", df.columns)
        self.assertIn("Gender", df.columns)
        
        # Check that there are no NaN values in critical columns
        self.assertFalse(df["Title"].isna().any())
        self.assertFalse(df["Price"].isna().any())
        
        # Check price conversion to IDR
        self.assertGreaterEqual(df["Price"].min(), 15.99 * 16000)

    def test_clean_existing_dataframe(self):
        """Test the clean_existing_dataframe function cleans problematic data"""
        # Create a DataFrame with problematic data
        problematic_df = pd.DataFrame({
            "Title": ["Product A", "", "Product B", "Product C", None],
            "Price": [1000, 2000, np.nan, "NaN", 5000],
            "Rating": [4.5, 3.8, 4.0, 3.9, 4.2],
            "Colors": [3, 2, 5, 4, 3],
            "Size": ["M", "L", "S", "XL", "XXL"],
            "Gender": ["Men", "Women", "Unisex", "Men", "Women"]
        })
        
        cleaned_df = clean_existing_dataframe(problematic_df)
        
        # Check that problematic rows are removed
        self.assertEqual(len(cleaned_df), 2)  # Only 2 valid rows should remain
        
        # Check that no empty titles exist
        self.assertFalse((cleaned_df["Title"] == "").any())
        self.assertFalse(cleaned_df["Title"].isna().any())
        
        # Check that no NaN prices exist
        self.assertFalse(cleaned_df["Price"].isna().any())
        
        # Verify the remaining rows are the expected ones
        self.assertIn("Product A", cleaned_df["Title"].values)
        self.assertIn(1000, cleaned_df["Price"].values)
        self.assertIn(5000, cleaned_df["Price"].values)

    def test_edge_cases(self):
        """Test edge cases like empty lists and unusual values"""
        # Test with empty list
        empty_result = transform_data([])
        self.assertEqual(empty_result, [])
        
        empty_df = transform_to_DataFrame([])
        self.assertTrue(empty_df.empty)
        
        # Test with unusual price formats
        unusual_data = [
            {
                "Title": "Special Product",
                "Price": "$1,234.56",  # Comma in price
                "Rating": "4.9/5",
                "Colors": "2 colors",
                "Size": "M",
                "Gender": "Unisex"
            },
            {
                "Title": "Discount Item",
                "Price": "$99.99 $79.99",  # Multiple prices
                "Rating": "4.2/5",
                "Colors": "3 colors",
                "Size": "L",
                "Gender": "Men"
            }
        ]
        
        # The regex should extract the first number it finds
        transformed = transform_data(unusual_data)
        self.assertEqual(len(transformed), 2)
        self.assertEqual(transformed[0]["Price"], 1234.56 * 16000)
        self.assertEqual(transformed[1]["Price"], 99.99 * 16000)

if __name__ == "__main__":
    unittest.main()