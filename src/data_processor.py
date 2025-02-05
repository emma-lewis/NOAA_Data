import pandas as pd
import logging

class DataProcessor:
    """Processes and standardizes WCGBTS data."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_data(self, df):
        """Cleans and standardizes data."""
        if df.empty:
            self.logger.warning("No data to process.")
            return df

        # Add survey name
        df["Survey"] = "WCGBTS"

        # Add columns
        df["Tow_Type"] = "Aberdeen Trawl"
        df["Tow_Depth_Category"] = "B"

        # Rename columns to match standard
        df = df.rename(columns={
            "date_yyyymmdd": "Year_Month_Day",
            "depth_m": "Bottom_Depth_M",
            "latitude_dd": "Latitude",
            "longitude_dd": "Longitude",
            "total_catch_numbers": "Catch_Numbers",
            "total_catch_wt_kg": "Catch_Wt_Kg",
            "cpue_kg_per_ha_der": "Cpue_Kg_Per_Ha_Der",
            "cpue_numbers_per_ha_der": "Cpue_Numbers_Per_Ha_Der",
            "scientific_name": "Scientific_Name",
            "common_name": "Common_Name",
            "subsample_count": "Subsample_Count",
            "subsample_wt_kg": "Subsample_Wt_Kg",
            "performance": "Performance"
        })

        # Convert date column
        df["Year_Month_Day"] = pd.to_datetime(df["Year_Month_Day"], format="%Y%m%d")
        df["Year"] = df["Year_Month_Day"].dt.year
        df["Month"] = df["Year_Month_Day"].dt.month
        df["Day"] = df["Year_Month_Day"].dt.day

        # Lowercase text fields
        df["Scientific_Name"] = df["Scientific_Name"].str.lower()
        df["Common_Name"] = df["Common_Name"].str.lower()

        # Map performance values
        performance_mapping = {
            "Satisfactory": 0,
            "Unsatisfactory": 1,
            "Intermediate": 2
        }
        df["Performance"] = df["Performance"].map(performance_mapping).fillna(-1).astype(int)

        # Convert CPUE per hectare to per m2
        df["Cpue_Wt_Kg_per_m2"] = df["Cpue_Kg_Per_Ha_Der"] / 10000
        df["Cpue_Numbers_per_m2"] = df["Cpue_Numbers_Per_Ha_Der"] / 10000

        return df