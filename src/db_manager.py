import os
import logging
import psycopg2
from psycopg2 import sql

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "noaa_data"),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

class Database:
    def __init__(self):
        """Initialize and connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            logging.info("Connected to PostgreSQL database.")
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_tables(self):
        """Create the wcgbts_data table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS wcgbts_data (
            id SERIAL PRIMARY KEY,
            year INT,
            month INT,
            day INT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            bottom_depth_m DOUBLE PRECISION,
            scientific_name TEXT,
            common_name TEXT,
            catch_numbers INT,
            catch_wt_kg DOUBLE PRECISION,
            cpue_wt_kg_per_m2 DOUBLE PRECISION,
            cpue_numbers_per_m2 DOUBLE PRECISION,
            subsample_count INT,
            subsample_wt_kg DOUBLE PRECISION,
            performance TEXT
        );
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            logging.info("Tables created successfully.")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Failed to create tables: {e}")
            raise

    def insert_wcgbts_data(self, df):
        """Insert cleaned CSV data into PostgreSQL."""
        insert_query = """
            INSERT INTO wcgbts_data (
                year, month, latitude, longitude, bottom_depth_m, 
                scientific_name, catch_numbers, catch_wt_kg, cpue_wt_kg_per_m2
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        records = [tuple(row) for row in df.itertuples(index=False, name=None)]
    
        try:
            self.cursor.executemany(insert_query, records)
            self.conn.commit()
            logging.info(f"Successfully inserted {len(df)} records into wcgbts_data.")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error inserting data: {e}")

    def close_connection(self):
        """Close database connection."""
        self.cursor.close()
        self.conn.close()
        logging.info("Database connection closed.")