FROM apache/airflow:2.10.2-python3.11

ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt