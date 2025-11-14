# COVID-Tracking-Project Notebooks

This folder contains the main exploratory and analytical notebooks for the COVID-Tracking-Project. These notebooks provide step-by-step data exploration, cleaning validation, and analysis of national and state-level COVID-19 trends.

## Notebook Overview

1. **[01_raw_data_exploration.ipynb](01_raw_data_exploration.ipynb)**
- **Purpose:** Preview and inspect raw data downloaded into `data/raw/`
- **Key Features:** Understand the raw data structure and identify fields that require cleaning.

2. **[02_cleaning_checks.ipynb](02_cleaning_checks.ipynb)**
- **Purpose:** Verify the outputs produced by `clean_data.py`.
- **Key Features:** Confirms formatting and checks transformations.

3. **[03_national_trends.ipynb](03_national_trends.ipynb)**
- **Purpose:** 
- **Key Features:** 

4. **[04_state_level_analysis.ipynb](04_state_level_analysis.ipynb)**
- **Purpose:** Find some patterns between the state level data.
- **Key Features:** Query data and use data visulization tools to figure out insights.


## Getting Started

### Prerequisites

These notebooks assume that:
- Your Python environment is already set up
- Raw data has been fetched 
- Cleaned data is available in `data/processed/`  

Note: If you have followed the instructions in the main project `README.md`, you are ready to run any notebook in this folder.

### Running the Notebooks

To launch Jupyter:

```bash
jupyter lab
```

You may run the notebooks in any order, but the recommended flow is:

1. Start with `01_raw_data_exploration.ipynb` to understand the incoming raw data
2. Continue with `02_cleaning_checks.ipynb` to verify the cleaning pipeline
3. Explore national-level insights in `03_national_trends.ipynb`
4. Use `04_state_level_analysis.ipynb` for trends across states