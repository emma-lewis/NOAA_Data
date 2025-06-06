import os
import logging
import pandas as pd
from sqlalchemy import create_engine

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Environment variables for DB config
DB_NAME = os.getenv("DB_NAME", "noaa_data")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Query1: Most prevalent species
query_prevalent = """SELECT scientific_name, COUNT(*) AS occurrence
FROM wcgbts_data
GROUP BY scientific_name
ORDER BY occurrence DESC
LIMIT 10;"""

# Query 2: Most caught species (by total individuals)
query_caught = """
SELECT scientific_name, SUM(catch_numbers) AS total_individuals
FROM wcgbts_data
GROUP BY scientific_name
ORDER BY total_individuals DESC
LIMIT 10;
"""

def main():
    """Fetch and print most prevalent and most caught species."""
    try:
        engine = create_engine(DATABASE_URL)
        logging.info("Connected to database.")

        # Most prevalent species
        df_prevalent = pd.read_sql_query(query_prevalent, engine)
        print("\nTop 10 Most Prevalent Species (by sampling events):")
        print(df_prevalent)

        # Most caught species
        df_caught = pd.read_sql_query(query_caught, engine)
        print("\nTop 10 Most Caught Species (by total individuals):")
        print(df_caught)

    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
    finally:
        engine.dispose()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()