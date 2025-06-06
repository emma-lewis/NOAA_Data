import os
import logging
import pandas as pd
from src.db_manager import Database

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_DIR = "data"
CSV_FILE_PATH = os.path.join(DATA_DIR, "wcgbts_data.csv")
CSV_URL = "https://www.webapps.nwfsc.noaa.gov/data/api/v1/source/trawl.catch_fact/selection.csv"

def download_csv():
    """Download WCGBTS data if not already downloaded."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if os.path.exists(CSV_FILE_PATH):
        logging.info(f"CSV file already exists: {CSV_FILE_PATH}")
        return CSV_FILE_PATH

    try:
        logging.info(f"Downloading CSV file from {CSV_URL}")
        df = pd.read_csv(CSV_URL)
    
        if df.empty:
            logging.error("Downloaded file is empty!")
            return None
    
        df.to_csv(CSV_FILE_PATH, index=False)
        logging.info(f"CSV file downloaded successfully: {CSV_FILE_PATH}")
        return CSV_FILE_PATH
    
    except Exception as e:
        logging.error(f"Error downloading or saving CSV: {e}")
        return None

def clean_dataframe(df):
    """Clean and standardize the data before inserting into the database."""
    logging.info("Cleaning and formatting data...")

    # Rename columns for consistency
    df.rename(columns={
        "date_yyyymmdd": "Year",
        "latitude_dd": "Latitude",
        "longitude_dd": "Longitude",
        "depth_m": "Bottom_Depth_M",
        "scientific_name": "Scientific_Name",
        "total_catch_numbers": "Catch_Numbers",
        "total_catch_wt_kg": "Catch_Wt_Kg",
        "cpue_kg_per_ha_der": "Cpue_Wt_Kg_per_m2",
    }, inplace=True)

    # Convert date column
    df["Year"] = pd.to_datetime(df["Year"], format="%Y%m%d", errors="coerce")
    df["Month"] = df["Year"].dt.month.fillna(1).astype(int)
    df["Year"] = df["Year"].dt.year

    # Ensure Month is not NaN
    df["Month"] = df["Month"].fillna(1).astype(int)  # Default to January (1) if missing

    # Convert text fields to lowercase
    df["Scientific_Name"] = df["Scientific_Name"].str.lower()

    # Convert numeric columns safely
    numeric_cols = ["Bottom_Depth_M", "Latitude", "Longitude", "Catch_Numbers", "Catch_Wt_Kg", "Cpue_Wt_Kg_per_m2"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Handle numeric values
    df["Catch_Numbers"] = pd.to_numeric(df["Catch_Numbers"], errors="coerce").fillna(0).astype("int64")
    df["Catch_Wt_Kg"] = pd.to_numeric(df["Catch_Wt_Kg"], errors="coerce").fillna(0).astype(float)
    df["Cpue_Wt_Kg_per_m2"] = pd.to_numeric(df["Cpue_Wt_Kg_per_m2"], errors="coerce").fillna(0).astype(float)

    # Drop unnecessary columns
    df = df[["Year", "Month", "Latitude", "Longitude", "Bottom_Depth_M",
             "Scientific_Name", "Catch_Numbers", "Catch_Wt_Kg", "Cpue_Wt_Kg_per_m2"]]

    logging.info("Data cleaned successfully!")
    return df

def main():
    """Main ETL process: download, clean, and insert WCGBTS data into PostgreSQL."""
    logging.info("Starting NOAA Data Processing")

    csv_path = download_csv()
    if not csv_path:
        logging.error("No valid CSV file found. Exiting.")
        return

    try:
        df = pd.read_csv(csv_path, low_memory=False)
        logging.info(f"Loaded {len(df)} rows from CSV.")
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        return
    
    df = clean_dataframe(df)

    logging.info(f"Inserting {len(df)} rows into the database...")

    try:
        db = Database()
        db.create_tables()
        db.insert_wcgbts_data(df)
        db.close_connection()
    except Exception as e:
        logging.error(f"Database operation failed: {e}")

if __name__ == "__main__":
    main()