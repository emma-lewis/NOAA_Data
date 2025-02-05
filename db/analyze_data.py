from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_URL = "postgresql://emma:password@localhost:5432/noaa_data"
engine = create_engine(DATABASE_URL)

# Query 1: Total Catch Weight by Year
query_catch_weight = """
SELECT year, SUM(catch_wt_kg) AS total_catch_weight
FROM wcgbts_data
GROUP BY year
ORDER BY year;
"""
df_catch_weight = pd.read_sql_query(query_catch_weight, engine)

# Query 2: Species Count per Year
query_species = """
SELECT year, COUNT(DISTINCT scientific_name) AS species_count
FROM wcgbts_data
GROUP BY year
ORDER BY year;
"""
df_species = pd.read_sql_query(query_species, engine)

engine.dispose()

# Check if queries returned data
if df_catch_weight.empty:
    print("No data found for catch weight.")
else:
    plt.figure(figsize=(10, 5))
    plt.plot(df_catch_weight["year"], df_catch_weight["total_catch_weight"], marker="o")
    plt.xlabel("Year")
    plt.ylabel("Total Catch Weight (kg)")
    plt.title("Total Catch Weight Over Time")
    plt.grid()
    plt.show()

if df_species.empty:
    print("No data found for species count.")
else:
    plt.figure(figsize=(10, 5))
    plt.bar(df_species["year"], df_species["species_count"])
    plt.xlabel("Year")
    plt.ylabel("Species Count")
    plt.title("Species Count by Year")
    plt.show()