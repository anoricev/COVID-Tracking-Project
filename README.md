# COVID-Tracking-Project

This is the final project for MLDS-400: Topics in Data Engineering.

## Repository Structure (subject to change)

```
COVID-Tracking-Project/
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │    └── .gitkeep
│   ├── processed/
│   │    └── .gitkeep
│   └── covid.db
│
├── src/
│   ├── fetch_covid_data.sh
│   ├── build_database.py
│   ├── clean_data.py
│   ├── aggregate_metrics.py
│   ├── utils.py
│   └── ...
│
├── notebooks/
│   ├── README.md
│   ├── 01_raw_data_exploration.ipynb
│   ├── 02_cleaning_checks.ipynb
│   ├── 03_national_trends.ipynb
│   ├── 04_state_level_analysis.ipynb
│   └── ...
│
└── reports/
    ├── README.md
    ├── figures/ 
    │   └── ...
    ├── tables/
    │   └── ...
    └── final_presentation.pptx

```