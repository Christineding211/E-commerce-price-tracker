import os

from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.mysql_to_gcs import MySQLToGCSOperator


TABLE_NAME = "product_price_timeline"


def _get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _validate_cloud_analytics_config() -> None:
    required_env_names = [
        "GCP_PROJECT_ID",
        "GCS_BUCKET",
        "BQ_DATASET",
    ]

    missing_env_names = [
        env_name for env_name in required_env_names if _get_env(env_name) == ""
    ]

    if missing_env_names:
        raise ValueError(
            "Missing required cloud analytics environment variables: "
            + ", ".join(missing_env_names)
        )


def create_product_price_timeline_cloud_tasks():
    project_id = _get_env("GCP_PROJECT_ID")
    bucket_name = _get_env("GCS_BUCKET")
    dataset_id = _get_env("BQ_DATASET")
    location = _get_env("BQ_LOCATION", "us-central1")

    gcs_object = (
        "mysql_exports/product_price_timeline/"
        "product_price_timeline_{{ ds_nodash }}_{}.csv"
    )
    gcs_load_pattern = (
        "mysql_exports/product_price_timeline/"
        "product_price_timeline_{{ ds_nodash }}_*.csv"
    )

    validate_config_task = PythonOperator(
        task_id="validate_product_price_timeline_cloud_config",
        python_callable=_validate_cloud_analytics_config,
    )

    export_to_gcs_task = MySQLToGCSOperator(
        task_id="export_product_price_timeline_to_gcs",
        mysql_conn_id="mysql_default",
        bucket=bucket_name,
        filename=gcs_object,
        sql=f"SELECT * FROM {TABLE_NAME}",
        export_format="csv",
    )

    load_to_bigquery_task = GCSToBigQueryOperator(
        task_id="load_product_price_timeline_to_bigquery",
        bucket=bucket_name,
        source_objects=[gcs_load_pattern],
        destination_project_dataset_table=(
            f"{project_id}.{dataset_id}.{TABLE_NAME}"
        ),
        source_format="CSV",
        autodetect=True,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        location=location,
    )

    validate_config_task >> export_to_gcs_task >> load_to_bigquery_task

    return validate_config_task, export_to_gcs_task, load_to_bigquery_task
