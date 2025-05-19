import re
import pandas as pd

# Define dirty patterns for data cleaning
DIRTY_PATTERNS = {
    "Title": ["Unknown Product", "No title"],
    "Rating": ["Invalid Rating / 5", "Not Rated", None],
    "Price": ["Price Unavailable", "Price Not Found", None]
}

def transform_data(data_list):
    """
    Transform a list of product dictionaries according to requirements
    
    Args:
        data_list: List of product dictionaries from web scraping
        
    Returns:
        List of transformed product dictionaries
    """
    transformed_list = []
    
    for product in data_list:
        transformed_product = {}
        
        # Transform Title - handle missing/invalid titles
        title = product.get("Title")
        if title and title not in DIRTY_PATTERNS["Title"]:
            transformed_product["Title"] = title
        else:
            transformed_product["Title"] = None
            
        # Transform Price - convert to IDR
        price = product.get("Price")
        if price and price not in DIRTY_PATTERNS["Price"]:
            # Extract numeric value and convert to IDR
            price_match = re.search(r'\$(\d+\.?\d*)', price)
            if price_match:
                try:
                    price_value = float(price_match.group(1))
                    transformed_product["Price"] = price_value * 16000  # Convert to IDR
                except ValueError:
                    transformed_product["Price"] = None
            else:
                transformed_product["Price"] = None
        else:
            transformed_product["Price"] = None
            
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
        pandas DataFrame with transformed data
    """
    # Transform data
    transformed_data = transform_data(data_list)
    
    # Convert to DataFrame
    df = pd.DataFrame(transformed_data)
    
    return df