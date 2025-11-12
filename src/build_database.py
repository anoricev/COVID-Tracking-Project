import pandas as pd
import sqlite3

csv_path = "data/processed/states_daily_cleaned.csv"
db_path = "data/covid.db"
table = "states_daily_cleaned"

def main():
    df = pd.read_csv(csv_path)  
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
        

if __name__ == "__main__":
    main()