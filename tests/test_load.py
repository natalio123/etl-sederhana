import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import numpy as np
import json
import io
import sys
import os

# Fix the import to match your project structure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import store_to_postgre, save_to_json, save_to_csv


class TestLoadFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        # Create a sample DataFrame for testing
        self.test_df = pd.DataFrame({
            'title': ['Product 1', 'Product 2', 'Product 3'],
            'price': [19.99, 29.99, 39.99],
            'rating': [4.5, 3.8, 4.2],
            'colors': [3, 2, 4],
            'size': ['M', 'L', 'S'],
            'gender': ['Men', 'Women', 'Unisex']
        })
        
        # Sample dictionary data
        self.test_dict_data = [
            {
                'title': 'Product 1',
                'price': 19.99,
                'rating': 4.5,
                'colors': 3,
                'size': 'M',
                'gender': 'Men'
            },
            {
                'title': 'Product 2',
                'price': 29.99,
                'rating': 3.8,
                'colors': 2,
                'size': 'L',
                'gender': 'Women'
            }
        ]

    @patch('utils.load.execute_values')
    @patch('utils.load.psycopg2.connect')
    def test_store_to_postgre_success(self, mock_connect, mock_execute_values):
        """Test successful data storage to PostgreSQL."""
        # Set up the mock connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Configure the mock to return the connection and cursor
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Override encoding attribute that seems to be causing issues
        mock_cursor.connection = MagicMock()
        
        # Call the function with test data
        result = store_to_postgre(self.test_df)
        
        # Assertions
        self.assertTrue(result)
        mock_connect.assert_called_once()
        self.assertEqual(mock_cursor.execute.call_count, 1)  # For CREATE TABLE query
        mock_execute_values.assert_called_once()
        self.assertEqual(mock_conn.commit.call_count, 1)
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('utils.load.execute_values')
    @patch('utils.load.psycopg2.connect')
    def test_store_to_postgre_custom_params(self, mock_connect, mock_execute_values):
        """Test PostgreSQL storage with custom connection parameters."""
        # Set up the mock connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Configure the mock to return the connection and cursor
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Override encoding attribute that seems to be causing issues
        mock_cursor.connection = MagicMock()
        
        # Custom connection parameters
        custom_params = {
            "host": "test-host",
            "database": "test-db",
            "user": "test-user",
            "password": "test-pass",
            "port": 1234
        }
        
        # Call the function with test data and custom params
        result = store_to_postgre(self.test_df, "test_table", custom_params)
        
        # Assertions
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**custom_params)
        # Verify test_table is in the create table statement
        create_table_call = mock_cursor.execute.call_args[0][0]
        self.assertIn("test_table", create_table_call)
        mock_execute_values.assert_called_once()

    @patch('utils.load.psycopg2.connect')
    def test_store_to_postgre_failure(self, mock_connect):
        """Test handling of PostgreSQL connection failure."""
        # Make the connection raise an exception
        mock_connect.side_effect = Exception("Connection failed")
        
        # Call the function and check it handles the error
        result = store_to_postgre(self.test_df)
        
        # Assert result is False on failure
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_json_dataframe(self, mock_json_dump, mock_file_open):
        """Test saving DataFrame to JSON."""
        # Call the function with DataFrame
        result = save_to_json(self.test_df)
        
        # Check file was opened and written to
        mock_file_open.assert_called_once_with('transformed_products.json', 'w')
        mock_json_dump.assert_called_once()
        
        # Verify that dict format matches expected
        args, kwargs = mock_json_dump.call_args
        saved_data = args[0]
        self.assertEqual(len(saved_data), 3)  # 3 records in test DataFrame
        self.assertEqual(saved_data[0]['title'], 'Product 1')
        self.assertEqual(kwargs['indent'], 2)
        
        # Assert result
        self.assertTrue(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_json_dict_data(self, mock_json_dump, mock_file_open):
        """Test saving dictionary data to JSON."""
        # Call the function with dict data
        result = save_to_json(self.test_dict_data, 'custom_file.json')
        
        # Check file was opened with custom name
        mock_file_open.assert_called_once_with('custom_file.json', 'w')
        mock_json_dump.assert_called_once()
        
        # Assert input data was passed correctly
        args, kwargs = mock_json_dump.call_args
        self.assertEqual(args[0], self.test_dict_data)
        
        # Assert result
        self.assertTrue(result)

    @patch('builtins.open')
    def test_save_to_json_exception(self, mock_file_open):
        """Test error handling in save_to_json function."""
        # Make open raise an exception
        mock_file_open.side_effect = Exception("File error")
        
        # Call the function and check it handles the error
        result = save_to_json(self.test_df)
        
        # Assert result is False on failure
        self.assertFalse(result)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv_dataframe(self, mock_to_csv):
        """Test saving DataFrame to CSV."""
        # Call the function with DataFrame
        result = save_to_csv(self.test_df)
        
        # Check to_csv was called with correct parameters
        mock_to_csv.assert_called_once_with('products.csv', index=False)
        
        # Assert result
        self.assertTrue(result)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv_dict_data(self, mock_to_csv):
        """Test saving dictionary data to CSV."""
        # Call the function with dict data and custom path
        result = save_to_csv(self.test_dict_data, 'custom_file.csv')
        
        # Check to_csv was called with correct parameters
        mock_to_csv.assert_called_once_with('custom_file.csv', index=False)
        
        # Assert result
        self.assertTrue(result)

    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv_exception(self, mock_to_csv):
        """Test error handling in save_to_csv function."""
        # Make to_csv raise an exception
        mock_to_csv.side_effect = Exception("CSV error")
        
        # Call the function and check it handles the error
        result = save_to_csv(self.test_df)
        
        # Assert result is False on failure
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()