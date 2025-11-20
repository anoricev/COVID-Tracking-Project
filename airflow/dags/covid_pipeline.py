from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
import os

PROJECT_DIR = os.environ.get("COVID_PROJECT_DIR", "/opt/airflow/COVID-Tracking-Project")
VENV_ACT = f"source {PROJECT_DIR}/.venv/bin/activate"

with DAG(
    dag_id="covid_tracking_pipeline",
    default_args={'owner': 'airflow'},
    start_date=datetime(2025, 11, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Fetch new data from API
    fetch_data = BashOperator(
        task_id="fetch_data",
        bash_command=f"cd {PROJECT_DIR} && {VENV_ACT} && bash src/fetch_covid_data.sh",
    )

    # Clean and transform processed tables
    clean_data = BashOperator(
        task_id="clean_data",
        bash_command=f"cd {PROJECT_DIR} && {VENV_ACT} && python src/clean_data.py --raw-dir data/raw --out-dir data/processed",
    )

    # dummy operator for notebook analysis
    National_Level_Analysis = EmptyOperator(
        task_id="National_Level_Analysis",
    )

    # dummy operator for notebook analysis
    State_Level_Analysis = EmptyOperator(
        task_id="State_Level_Analysis",
    )

    # Run shiny app
    run_shiny = BashOperator(
        task_id="run_shiny_app",
        bash_command=f"cd {PROJECT_DIR} && {VENV_ACT} && shiny run --reload src/app.py",
        trigger_rule="all_done",
    )

    fetch_data >> clean_data >> National_Level_Analysis >> State_Level_Analysis >>run_shiny
