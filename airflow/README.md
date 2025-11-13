# Airflow stack for COVID Tracking Project

This folder contains a containerized Apache Airflow setup that orchestrates the project pipeline.

> **Note:** Airflow does not support Python 3.12+.
> This project uses **Python 3.11** in the main environment to ensure compatibility with Airflow and its dependencies.
> The container also run Python 3.11 internally.

## Start the stack

From the `airflow` folder run the following:

```bash
docker compose build --no-cache
docker compose up airflow-init
docker compose up -d
```

Now open the UI: 

- URL: [http://localhost:8080](http://localhost:8080)
- Username: airflow
- Password: airflow

In the UI toggle your DAG on then click the play button to trigger a run.

## Stop and clean up

```bash
docker compose down -v
```
