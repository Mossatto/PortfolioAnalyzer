import psycopg2
from .db_connector import create_connection, SCHEMA_NAME # Imports the connector and schema name

# ====================================================================
# DEFINITION OF DML QUERIES (Lowercase tables for PostgreSQL portability)
# ====================================================================

SQL_INSERT_USER = f"""
INSERT INTO "user" (user_name) 
VALUES ('Matheus Mossatto')
ON CONFLICT (user_id) DO NOTHING 
RETURNING user_id;
"""

SQL_INSERT_ASSETS = f"""
INSERT INTO asset (user_id, ticker, full_name, asset_type, sector)
VALUES
    (1, 'PETR4', 'Petroleo Brasileiro S.A. Pref', 'STOCK', 'Oil & Gas'),
    (1, 'BBDC4', 'Banco Bradesco S.A. Pref', 'STOCK', 'Financial Services'),
    (1, 'IVVB11', 'Ishares S&P 500 ETF', 'ETF', 'Diversified')
ON CONFLICT (ticker) DO NOTHING;
"""

SQL_INSERT_TRANSACTIONS = f"""
INSERT INTO transaction (asset_id, transaction_date, transaction_type, quantity, unit_price, total_value)
VALUES
    (1, '2024-01-10', 'BUY', 100, 30.50, 3050.00), 
    (2, '2024-02-15', 'BUY', 200, 14.20, 2840.00), 
    (1, '2024-03-20', 'DIVIDEND', 0, 0, 150.00); 
"""

def load_initial_data():
    """Connects to DB and executes all initial DML queries (ACID)."""
    
    conn = create_connection()
    if conn is None:
        return

    SQL_SET_SCHEMA = f"SET search_path TO {SCHEMA_NAME}, public;"
    
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_SET_SCHEMA) 
            
            # Execute all DML operations
            cur.execute(SQL_INSERT_USER)
            cur.execute(SQL_INSERT_ASSETS)
            cur.execute(SQL_INSERT_TRANSACTIONS)

            conn.commit() 
            print("🚀 Initial data load successful. Assets and Transactions are ready.")
            return True
            
    except Exception as e:
        print(f"❌ Error during data insertion. Operation ROLLED BACK: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
