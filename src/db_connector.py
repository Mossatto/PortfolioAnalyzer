import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables securely ! !!
load_dotenv()

# --- DATABASE CONFIGURATION ---
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

SCHEMA_NAME = "analyzer_schema"

def create_connection():
    """Establishes and returns the connection object (psycopg2)."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        # Note: We won't print connection success here to keep the layer silent.
        return conn
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to PostgreSQL. Details: {e}")
        return None
