import os
import requests
import pandas as pd

class NOAAClient:
    def __init__(self, download_dir="data"):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)

    def download_wcgbts_csv(self):
        """Download the WCGBTS dataset as a CSV file."""
        file_path = os.path.join(self.download_dir, "wcgbts_data.csv")
        url = "https://www.webapps.nwfsc.noaa.gov/data/api/v1/source/trawl.catch_fact/selection.csv"

        print(f"Downloading CSV file from {url}")
        headers = {"Accept": "text/csv"}  #Ensure the response is in CSV format
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if not response.text.strip():  #If response is empty
                print("API returned an empty response. No data downloaded.")
                return None

            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(response.text)

            print(f"CSV file downloaded successfully: {file_path}")
            return file_path
        else:
            print(f"Failed to download CSV: {response.status_code} - {response.text}")
            return None

    def load_wcgbts_data(self):
        """Load WCGBTS data from the downloaded CSV file."""
        file_path = os.path.join(self.download_dir, "wcgbts_data.csv")

        if os.path.exists(file_path):
            print(f"Loading CSV file: {file_path}")

            try:
                df = pd.read_csv(file_path, encoding="utf-8-sig")
                print(f"Loaded {len(df)} rows from CSV.")
                return df
            except pd.errors.EmptyDataError:
                print("The CSV file is empty. Please check the API or manually download it.")
                return pd.DataFrame()
        else:
            print("No CSV file found. Please download it manually.")
            return pd.DataFrame()
