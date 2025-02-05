from sqlalchemy import create_engine
import pandas as pd
import os

# Database connection details
DB_NAME = os.getenv("DB_NAME", "noaa_data")
USER = os.getenv("DB_USER", "emmalewis")
PASSWORD = os.getenv("DB_PASS", "password")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")

# Connect to PostgreSQL
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Query data
query = """SELECT scientific_name, COUNT(*) AS occurrence
FROM wcgbts_data
GROUP BY scientific_name
ORDER BY occurrence DESC
LIMIT 10;"""

df = pd.read_sql_query(query, engine)

# Display results
print(df)

# Close connection
engine.dispose()