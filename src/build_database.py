import pandas as pd
import sqlite3

# File paths
states_csv = "data/processed/states_daily_cleaned.csv"
us_csv = "data/processed/us_daily_cleaned.csv"
db_path = "data/covid.db"

# Table names in SQLite
states_table = "states_daily_cleaned"
us_table = "us_daily_cleaned"

def write_csv_to_db(csv_path, table_name, conn):
    """Helper: read CSV and write to SQLite."""
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✓ Loaded {csv_path} into table '{table_name}'")

def main():
    with sqlite3.connect(db_path) as conn:
        write_csv_to_db(states_csv, states_table, conn)
        write_csv_to_db(us_csv, us_table, conn)

    print("\nAll tables successfully written into covid.db!")

if __name__ == "__main__":
    main()
