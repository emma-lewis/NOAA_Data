import os
import logging
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Environment-based DB config
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "noaa_data")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Query 1: Total Catch Weight by Year
query_catch_weight = """
SELECT year, SUM(catch_wt_kg) AS total_catch_weight
FROM wcgbts_data
GROUP BY year
ORDER BY year;
"""

# Query 2: Species Count per Year
query_species = """
SELECT year, COUNT(DISTINCT scientific_name) AS species_count
FROM wcgbts_data
GROUP BY year
ORDER BY year;
"""

# Plot
def plot_total_catch_weight(df):
    df.plot(x="year", y="total_catch_weight", kind="line", marker="o", title="Total Catch Weight Over Time")
    plt.xlabel("Year")
    plt.ylabel("Total Catch Weight (kg)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('data/Total_Catch_Weight.png')
    plt.close()
    logging.info("Saved plot: data/Total_Catch_Weight.png")

def plot_species_count(df):
    df.plot(x='year', y='species_count', kind='bar', title='Species Count by Year')
    plt.xlabel("Year")
    plt.ylabel("Species Count")
    plt.tight_layout()
    plt.savefig('data/Species_Count.png')
    plt.close()
    logging.info("Saved plot: data/Species_Count.png")

def main():
    """Runs analysis queries and generates visualizations from wcgbts_data."""
    try:
        engine = create_engine(DATABASE_URL)
        logging.info("Connected to database.")

        df_catch_weight = pd.read_sql_query(query_catch_weight, engine)
        df_species_count = pd.read_sql_query(query_species, engine)

        plot_total_catch_weight(df_catch_weight)
        plot_species_count(df_species_count)

    except Exception as e:
        logging.error(f"Failed to analyze or plot data: {e}")
    finally:
        engine.dispose()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()   