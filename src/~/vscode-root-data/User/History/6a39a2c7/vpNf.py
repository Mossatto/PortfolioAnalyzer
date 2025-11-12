# [ ... imports and DB config remain the same ... ]
import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
SCHEMA_NAME = "analyzer_schema" 

def calculate_average_price():
    """Calculates the Average Acquisition Price (PM) for all assets."""
    
    conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
    
    # SQL Query (DML SELECT) - Simplificado
    SQL_QUERY = f"""
    SET search_path TO {SCHEMA_NAME}, public;
    SELECT 
        a.ticker,
        t.quantity,
        t.unit_price,
        t.transaction_type
    FROM 
        asset a  -- Minúscula e sem aspas
    JOIN 
        transaction t ON a.asset_id = t.asset_id -- Minúscula e sem aspas
    WHERE 
        t.transaction_type = 'BUY';
    """
    
    try:
        engine = psycopg2.connect(conn_string)
        df = pd.read_sql(SQL_QUERY, engine)
        engine.close()
        
        print("✅ Buy Transaction Data extracted successfully into Pandas DataFrame.")

        # [ ... Transformation Logic remains the same ... ]
        df['total_cost'] = df['quantity'] * df['unit_price']
        
        analysis = df.groupby('ticker').agg(
            total_cost_sum=('total_cost', 'sum'),
            total_quantity_sum=('quantity', 'sum')
        ).reset_index()
        
        analysis['average_price'] = analysis['total_cost_sum'] / analysis['total_quantity_sum']
        
        print("\n📊 Average Price Analysis Results:")
        print(analysis[['ticker', 'average_price']])
        
        return analysis[['ticker', 'average_price']]

    except Exception as e:
        print(f"❌ Error in data analysis or connection: {e}")
        return None

if __name__ == "__main__":
    calculate_average_price()