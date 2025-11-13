# COVID-Tracking-Project

This is the final project for MLDS-400: Topics in Data Engineering at Northwestern University. The project reproduces and extends the workflow of The COVID Tracking Project by building an automated data pipeline that fetches, stores, and explores COVID-19 case data across US states and the nation.

The project is implemented in Python and Shell scripting, featuring modular components for data ingestion, processing, and visualization, along with a Shiny for Python app for interactive exploration of state-level trends. The workflow is origanized using a Dockerized Apache Airflow stack, which provides automated scheduling of the full data pipeline.

## Repository Structure (subject to change)

```bash
COVID-Tracking-Project/
├── .gitignore
├── README.md
├── requirements.txt
│
├── airflow
│   ├── README.md
│   ├── dags
│   │    └── covid_pipeline.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── data/                                   # ignored
│   ├── raw/
│   ├── processed/
│   └── covid.db
│
├── src/
│   ├── fetch_covid_data.sh
│   ├── clean_data.py
│   ├── build_database.py
│   ├── app.py
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
python3.11 -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate       

# Install required packages
pip install -r requirements.txt
```

### 3. Load data

Use the provided shell script to download both JSON and CSV versions of national and state-level data into `data/raw/`.
This will download current and historical datasets for the US and all states.

```bash
bash src/fetch_covid_data.sh
```

After downloading the raw data, run the cleaning script to save the processed data to `data/processed`.
You can also compile the cleaned data into a structured database in `data`.

```bash
python src/clean_data.py
python src/build_database.py
```

## Files & Usage 

- `notebooks/`: Jupyter notebooks for exploration, checks, and analysis
- `reports/`: Exported figures and summary tables
- `src/`: Data processing scripts
- `airflow/`: Dockerized Airflow setup for automated pipeline scheduling
- `app.py`: Shiny App for interactive data exploration

```bash
# Launch Shiny App
shiny run src/app.py
```