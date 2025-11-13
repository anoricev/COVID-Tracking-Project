import pandas as pd
import numpy as np
import os


def clean_states_daily(
    input_path: str = "data/raw/states_daily.csv",
    output_path: str = "data/processed/states_daily_cleaned.csv",
):

    # --- Load Data ---
    input_path = 'data/raw/states_daily.csv'
    output_path = 'data/processed/states_daily_cleaned.csv'
    
    try:
        states_daily = pd.read_csv(input_path)
        print(f"Successfully loaded raw data from {input_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    df = states_daily.copy()

    # --- Cleaning ---
    # Remove columns that are deprecated and not informative for analysis
    deprecated_col = [
        'checkTimeEt', 'commercialScore', 'dateChecked', 'dateModified', 
        'grade', 'hash', 'hospitalized', 'negativeIncrease', 
        'negativeRegularScore', 'negativeScore', 'posNeg', 'positiveScore', 
        'score', 'total'
    ]
    non_informative_col = ['dataQualityGrade']
    df = df.drop(deprecated_col + non_informative_col, axis=1)

    # Convert 'date' and 'lastUpdateEt' from integers to datetime objects
    # Fill missing 'lastUpdateEt' values with the 'date' for that row
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df['lastUpdateEt'] = pd.to_datetime(df['lastUpdateEt'], errors='coerce')
    df['lastUpdateEt'] = df['lastUpdateEt'].fillna(df['date'])

    # Current columns: forward fill and fill remaining NaNs with 0
    df = df.sort_values(by=['state', 'date'])
    current_columns = ['hospitalizedCurrently', 'inIcuCurrently', 'onVentilatorCurrently']
    for col in current_columns:
        df[col] = df.groupby('state')[col].ffill()
    df[current_columns] = df[current_columns].fillna(0)

    # Cumulative columns: forward fill and enforce cumulative >= current
    cumulative_pairs = {
        'hospitalizedCumulative': 'hospitalizedCurrently',
        'inIcuCumulative': 'inIcuCurrently',
        'onVentilatorCumulative': 'onVentilatorCurrently'
    }
    for cum_col, cur_col in cumulative_pairs.items():
        df[cum_col] = df[cum_col].fillna(df[cur_col])
        df[cum_col] = df.groupby('state')[cum_col].cummax()
        df[cum_col] = np.maximum(df[cum_col], df[cur_col])

    # Fill all remaining NaNs in other numeric columns with 0
    all_numeric_cols = df.select_dtypes(include='number').columns
    df[all_numeric_cols] = df[all_numeric_cols].fillna(0)

    # --- Feature Engineering ---
    # Add growth dynamics
    df['positive_growth_rate'] = df.groupby('state')['positive'].pct_change().round(3)
    df['death_growth_rate'] = df.groupby('state')['death'].pct_change().round(3)

    # Add Ratios
    df['positivityRate'] = (df['positiveIncrease'] / df['totalTestResultsIncrease']).round(3)
    df['caseFatalityRate'] = (df['death'] / df['positive']).round(3)
    ratios = ['positivityRate', 'caseFatalityRate', 'positive_growth_rate', 'death_growth_rate']
    df[ratios] = df[ratios].replace([np.inf, -np.inf], np.nan).fillna(0)

    # --- Save Data ---
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df.to_csv(output_path, index=False)
    print(f"Successfully cleaned states data and saved to {output_path}")


def clean_us_daily(
    input_path: str = "data/raw/us_daily.csv",
    output_path: str = "data/processed/us_daily_cleaned.csv",
):

    input_path = "data/raw/us_daily.csv"
    output_path = "data/processed/us_daily_cleaned.csv"

    # Load data
    try:
        us_daily = pd.read_csv(input_path)
        print(f"Successfully loaded raw data from {input_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    df = us_daily.copy()

    # Drop deprecated or non-informative columns
    removed_cols = ['pending', 'dateChecked', 'lastModified', 'recovered', 'total', 'posNeg', 'hash']
    df = df.drop(columns=removed_cols)

    # Convert date and sort by time
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df = df.sort_values('date').reset_index(drop=True)

    # Forward fill missing current hospitalization data
    current_cols = ['hospitalizedCurrently', 'inIcuCurrently', 'onVentilatorCurrently']
    df[current_cols] = df[current_cols].ffill().fillna(0)

    # Keep cumulative counts increasing and at least as large as current values
    pairs = {
        'hospitalizedCumulative': 'hospitalizedCurrently',
        'inIcuCumulative': 'inIcuCurrently',
        'onVentilatorCumulative': 'onVentilatorCurrently'
    }
    for cum, cur in pairs.items():
        df[cum] = df[cum].fillna(df[cur]).cummax()
        df[cum] = np.maximum(df[cum], df[cur])

    # Fill any remaining numeric NaNs with 0
    df[df.select_dtypes('number').columns] = df.select_dtypes('number').fillna(0)

    # Fix totalTestResults if smaller than positive + negative, then recompute increases
    comp = (df['positive'].fillna(0) + df['negative'].fillna(0)).astype(float)
    df['totalTestResults'] = np.where(df['totalTestResults'] < comp, comp, df['totalTestResults'])
    df['totalTestResults'] = df['totalTestResults'].cummax()
    df['totalTestResultsIncrease'] = df['totalTestResults'].diff().fillna(0).clip(lower=0)

    # Recalculate daily increases from cumulative totals
    df['positiveIncrease'] = df['positive'].diff().fillna(0).clip(lower=0)
    df['negativeIncrease'] = df['negative'].diff().fillna(0).clip(lower=0)
    df['deathIncrease'] = df['death'].diff().fillna(0).clip(lower=0)
    df['hospitalizedIncrease'] = df['hospitalized'].diff().fillna(0).clip(lower=0)

    # Compute growth rates and key ratios
    df['positive_growth_rate'] = df['positive'].pct_change().round(3)
    df['death_growth_rate'] = df['death'].pct_change().round(3)
    df['positivityRate'] = (df['positiveIncrease'] / df['totalTestResultsIncrease']).round(3)
    df['caseFatalityRate'] = (df['death'] / df['positive']).round(3)

    # Replace infinities or NaNs in ratio columns
    cols = ['positivityRate', 'caseFatalityRate', 'positive_growth_rate', 'death_growth_rate']
    df[cols] = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0)

    # Save cleaned file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned U.S. daily data to {output_path}")


def main():
    """
    Run all cleaning pipelines.
    """
    clean_states_daily()
    clean_us_daily()


if __name__ == "__main__":
    main()
