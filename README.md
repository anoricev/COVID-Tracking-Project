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

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/anoricev/COVID-Tracking-Project.git
cd COVID-Tracking-Project
```

### 2. Set up the environment

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Load data

Use the provided shell script to download both JSON and CSV versions of national and state-level data into `data/raw/`.
This will download current and historical datasets for the US and all states.

```bash
bash src/fetch_covid_data.sh
```

### 4. Build a SQLite database (under construction)

Once the raw files are downloaded, you can compile them into a structured database in `data`.

```bash
python src/build_database.py
```