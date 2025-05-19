import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import json


def store_to_postgre(df, table_name="products", connection_params=None):
    """
    Store transformed DataFrame to PostgreSQL database
    
    Args:
        df: pandas DataFrame with transformed product data
        table_name: Target table name in PostgreSQL
        connection_params: Dictionary with connection parameters
            Example: {
                "host": "localhost",
                "database": "product_db",
                "user": "postgres",
                "password": "password"
            }
    
    Returns:
        Boolean indicating success or failure
    """
    if connection_params is None:
        connection_params = {
            "host": "localhost",
            "database": "product_db",
            "user": "developer",
            "password": "secretpassword",
            "port": 5432
        }
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            price NUMERIC,
            rating NUMERIC,
            colors INTEGER,
            size VARCHAR(50),
            gender VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        
        # Prepare data for insert
        columns = list(df.columns)
        values = [tuple(x) for x in df.to_numpy()]
        
        # Insert data
        insert_query = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES %s
        """
        execute_values(cursor, insert_query, values)
        
        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully stored {len(df)} records to {table_name} table")
        return True
        
    except Exception as e:
        print(f"Error storing data to PostgreSQL: {e}")
        return False


def save_to_json(data, file_path="transformed_products.json"):
    """
    Save transformed data to a JSON file
    
    Args:
        data: List of transformed product dictionaries or DataFrame
        file_path: Path to save the JSON file
    
    Returns:
        Boolean indicating success or failure
    """
    try:
        # Convert DataFrame to list of dictionaries if needed
        if isinstance(data, pd.DataFrame):
            data_to_save = data.to_dict(orient='records')
        else:
            data_to_save = data
            
        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=2)
            
        print(f"Data successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
        return False


def save_to_csv(data, file_path="products.csv"):
    """
    Save transformed data to a CSV file
    
    Args:
        data: List of transformed product dictionaries or DataFrame
        file_path: Path to save the CSV file
    
    Returns:
        Boolean indicating success or failure
    """
    try:
        # Convert list of dictionaries to DataFrame if needed
        if not isinstance(data, pd.DataFrame):
            df_to_save = pd.DataFrame(data)
        else:
            df_to_save = data
            
        # Save the DataFrame to CSV
        df_to_save.to_csv(file_path, index=False)
            
        print(f"Data successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving data to CSV: {e}")
        return False
