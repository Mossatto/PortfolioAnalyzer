from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
SCHEMA_NAME = "analyzer_schema"


def create_connection():
    # [ ... create_connection function remains the same ... ]
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("✅ PostgreSQL connection established successfully.")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL. Check your .env credentials and DB status. Details: {e}")
        return None


def insert_initial_data(conn):
    """Inserts an initial user and sample assets (DML practice)."""
    
    # Set the search_path to ensure commands run in the correct schema
    SQL_SET_SCHEMA = f"SET search_path TO {SCHEMA_NAME}, public;"
    
    # 1. SQL for inserting a User (Simplificado: Removido aspas duplas e prefixos)
    SQL_INSERT_USER = f"""
    INSERT INTO "user" (user_name) 
    VALUES ('Matheus Mossatto')
    ON CONFLICT (user_id) DO NOTHING 
    RETURNING user_id;
    """
    
    # 2. SQL for inserting sample Assets (Simplificado)
    SQL_INSERT_ASSETS = f"""
    INSERT INTO asset (user_id, ticker, full_name, asset_type, sector)
    VALUES
        (1, 'PETR4', 'Petroleo Brasileiro S.A. Pref', 'STOCK', 'Oil & Gas'),
        (1, 'BBDC4', 'Banco Bradesco S.A. Pref', 'STOCK', 'Financial Services'),
        (1, 'IVVB11', 'Ishares S&P 500 ETF', 'ETF', 'Diversified')
    ON CONFLICT (ticker) DO NOTHING;
    """
    
    # 3. SQL for inserting Mock Transactions (Simplificado)
    SQL_INSERT_TRANSACTIONS = f"""
    INSERT INTO transaction (asset_id, transaction_date, transaction_type, quantity, unit_price, total_value)
    VALUES
        (1, '2024-01-10', 'BUY', 100, 30.50, 3050.00), 
        (2, '2024-02-15', 'BUY', 200, 14.20, 2840.00), 
        (1, '2024-03-20', 'DIVIDEND', 0, 0, 150.00); 
    """

    try:
        with conn.cursor() as cur:
            cur.execute(SQL_SET_SCHEMA) 
            
            cur.execute(SQL_INSERT_USER)
            user_id = cur.fetchone()[0] if cur.rowcount > 0 else 1
            print(f"👤 Base User inserted/existing with ID: {user_id}")

            cur.execute(SQL_INSERT_ASSETS)
            cur.execute(SQL_INSERT_TRANSACTIONS)

            conn.commit() 
            print("🚀 Initial data (User, Assets, and Transactions) inserted successfully.")
    except Exception as e:
        print(f"❌ Error during data insertion. Operation ROLLED BACK: {e}")
        conn.rollback()


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        insert_initial_data(conn)
        conn.close()