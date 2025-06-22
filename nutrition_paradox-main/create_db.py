import sqlite3
import pandas as pd

# Load cleaned data
df_obesity_clean = pd.read_csv("obesity_data.csv")
df_malnutrition_clean = pd.read_csv("malnutrition_data.csv")

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("nutrition_data.db")
cursor = conn.cursor()

# Create 'obesity' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS obesity (
    indicator TEXT,
    country TEXT,
    region TEXT,
    year INTEGER,
    sex TEXT,
    value REAL,
    age_group TEXT
)
""")

# Create 'malnutrition' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS malnutrition (
    indicator TEXT,
    country TEXT,
    region TEXT,
    year INTEGER,
    sex TEXT,
    value REAL,
    age_group TEXT
)
""")

# Commit schema creation
conn.commit()

# Insert clean data into the tables
df_obesity_clean.to_sql('obesity', conn, if_exists='append', index=False)
df_malnutrition_clean.to_sql('malnutrition', conn, if_exists='append', index=False)

print("Tables created and data inserted successfully!")
