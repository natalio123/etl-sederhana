import re
import pandas as pd
import numpy as np

# Define dirty patterns for data cleaning
DIRTY_PATTERNS = {
    "Title": ["Unknown Product", "No title", "", None],  # Added empty string
    "Rating": ["Invalid Rating / 5", "Not Rated", None],
    "Price": ["Price Unavailable", "Price Not Found", None]
}

def transform_data(data_list):
    """
    Transform a list of product dictionaries according to requirements
    
    Args:
        data_list: List of product dictionaries from web scraping
        
    Returns:
        List of transformed product dictionaries with no empty titles or NaN prices
    """
    transformed_list = []
    
    for product in data_list:
        transformed_product = {}
        
        # Transform Title - handle missing/invalid titles
        title = product.get("Title", "").strip()  # Get title with default empty string and strip whitespace
        if title and title not in DIRTY_PATTERNS["Title"]:
            transformed_product["Title"] = title
        else:
            # Skip products with missing titles instead of adding them with None value
            continue
            
        # Transform Price - convert to IDR
        price = product.get("Price")
        if price and price not in DIRTY_PATTERNS["Price"]:
            # Extract numeric value and convert to IDR
            price_match =  re.search(r'\$([\d,]+\.?\d*)', price)
            if price_match:
                try:
                    # Remove commas for numbers like $1,234.56
                    price_str = price_match.group(1).replace(',', '')
                    price_value = float(price_str)
                    transformed_product["Price"] = price_value * 16000  # Convert to IDR
                except ValueError:
                    # Skip products with invalid prices
                    continue
            else:
                # Skip products with unparseable prices
                continue
        else:
            # Skip products with missing prices
            continue
            
        # Transform Rating - convert to float
        rating = product.get("Rating")
        if rating and rating not in DIRTY_PATTERNS["Rating"]:
            # Extract numeric rating using regex
            rating_match = re.search(r'(\d+\.?\d*)', rating)
            if rating_match:
                try:
                    transformed_product["Rating"] = float(rating_match.group(1))
                except ValueError:
                    transformed_product["Rating"] = None
            else:
                transformed_product["Rating"] = None
        else:
            transformed_product["Rating"] = None
            
        # Transform Colors - extract numeric value
        colors = product.get("Colors")
        if colors:
            colors_match = re.search(r'(\d+)', colors)
            if colors_match:
                transformed_product["Colors"] = int(colors_match.group(1))
            else:
                transformed_product["Colors"] = None
        else:
            transformed_product["Colors"] = None
            
        # Transform Size - already cleaned during extraction, just copy
        size = product.get("Size")
        transformed_product["Size"] = size
            
        # Transform Gender - already cleaned during extraction, just copy
        gender = product.get("Gender")
        transformed_product["Gender"] = gender
        
        transformed_list.append(transformed_product)
    
    return transformed_list

def transform_to_DataFrame(data_list):
    """
    Convert transformed data list to pandas DataFrame
    
    Args:
        data_list: List of transformed product dictionaries
        
    Returns:
        pandas DataFrame with transformed data, no empty titles or NaN prices
    """
    # Transform data
    transformed_data = transform_data(data_list)
    
    # Convert to DataFrame
    df = pd.DataFrame(transformed_data)
    
    # Additional data cleaning to ensure no NaN values for critical columns
    if not df.empty:
        # Drop rows with missing titles or prices (shouldn't happen with the improved transform_data)
        df = df.dropna(subset=["Title", "Price"])
        
        # Check for NaN values as strings in the Price column
        df = df[~df["Price"].astype(str).str.contains("nan|NaN|NAN")]
    
    return df

# Clean existing dataframe with problematic data
def clean_existing_dataframe(df):
    """
    Clean an existing DataFrame that already has empty titles and NaN prices
    
    Args:
        df: pandas DataFrame with problematic data
        
    Returns:
        Cleaned pandas DataFrame
    """
    # Make a copy to avoid modifying the original
    cleaned_df = df.copy()
    
    # Drop rows with empty titles or None
    cleaned_df = cleaned_df[cleaned_df["Title"].notna() & (cleaned_df["Title"] != "")]
    
    # Filter out NaN values and 'NaN' strings in the Price column
    # Important: treat numeric values and string values differently
    # First handle actual NaN values
    cleaned_df = cleaned_df.dropna(subset=["Price"])
    
    # Then handle string 'NaN' values - but only for string type columns
    # Check each value - if it's a string, check if it contains 'NaN'
    str_nan_rows = []
    for idx, value in enumerate(cleaned_df["Price"]):
        # Only check string values
        if isinstance(value, str) and ("nan" in value.lower() or "NaN" in value or "NAN" in value):
            str_nan_rows.append(idx)
    
    # Drop rows that have 'NaN' as a string
    cleaned_df = cleaned_df.drop(str_nan_rows)
    
    return cleaned_df