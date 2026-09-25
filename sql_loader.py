import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import time

print("Initializing Enterprise SQL Data Loader...")

# 1. Load the generated DataFrames into memory
print("Reading CSV files...")
df_spend = pd.read_csv('normalized_cloud_spend.csv')
df_zombies = pd.read_csv('zombie_resources.csv')
df_forecast = pd.read_csv('cost_forecast.csv')

# 2. Build the SQLAlchemy Connection String
# Using your exact local SSMS server name and the fast_executemany flag
params = urllib.parse.quote_plus(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-GEC0TTHB\MSSQL;'
    r'DATABASE=EnterpriseFinOps;'
    r'Trusted_Connection=yes;'
)

# Engine configured for maximum write speed
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

# 3. Bulk Insert Data
start_time = time.time()

print(f"\nLoading Fact_CloudSpend ({len(df_spend):,} rows)...")
# if_exists='replace' will automatically create the SQL tables based on Pandas data types
df_spend.to_sql('Fact_CloudSpend', engine, if_exists='replace', index=False)

print(f"Loading Dim_ZombieResources ({len(df_zombies):,} rows)...")
df_zombies.to_sql('Dim_ZombieResources', engine, if_exists='replace', index=False)

print(f"Loading Fact_CostForecast ({len(df_forecast):,} rows)...")
df_forecast.to_sql('Fact_CostForecast', engine, if_exists='replace', index=False)

elapsed_time = round(time.time() - start_time, 2)
print(f"\nSUCCESS! 🚀 All Data loaded into SQL Server in {elapsed_time} seconds.")