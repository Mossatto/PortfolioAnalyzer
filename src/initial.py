
from .data_repository import load_initial_data

if __name__ == "__main__":
    if load_initial_data():
        print("✅ Database setup complete and data loaded successfully.")
    else:
        print("🛑 Initial data load failed.")
