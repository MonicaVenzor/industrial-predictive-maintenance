from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow/project"

default_args = {
    "owner": "monica_venzor",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="predictive_maintenance_pipeline",
    description="Pipeline end-to-end: ingesta, transformacion dbt y prediccion XGBoost",
    schedule_interval="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["predictive_maintenance", "manufacturing"],
) as dag:

    ingesta = BashOperator(
        task_id="ingest_raw_data",
        bash_command=f"cd {PROJECT_DIR} && python src/ingestion/load_raw.py",
    )

    transformacion = BashOperator(
        task_id="dbt_run_staging_and_marts",
        bash_command=f"cd {PROJECT_DIR}/dbt/predictive_maintenance && dbt run",
    )

    tests = BashOperator(
        task_id="dbt_test_data_quality",
        bash_command=f"cd {PROJECT_DIR}/dbt/predictive_maintenance && dbt test",
    )

    prediccion = BashOperator(
        task_id="run_failure_prediction",
        bash_command=f"cd {PROJECT_DIR} && python src/models/save_model.py",
    )

    ingesta >> transformacion >> tests >> prediccion
