import os
import sys
from typing import List

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

VIEWS: List[str] = [
    "daily_best_deals",
    "platform_price_diff",
    "product_price_timeline",
]

def get_required_env(name: str):
    """Read a required environment variable and stop early if it is missing."""
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise ValueError(f"Missing required environment variable: {name}")

    return value.strip()

def create_mysql_engine() -> Engine:
    """Create a SQLAlchemy connection engine for MySQL."""
    mysql_host = get_required_env("MYSQL_HOST")
    mysql_port = get_required_env("MYSQL_PORT")
    mysql_account = get_required_env("MYSQL_ACCOUNT")
    mysql_password = get_required_env("MYSQL_PASSWORD")
    mysql_database = get_required_env("MYSQL_DATABASE")

    mysql_url = (
        f"mysql+pymysql://{mysql_account}:{mysql_password}"
        f"@{mysql_host}:{mysql_port}/{mysql_database}"
    )

    return create_engine(mysql_url)

def ensure_bigquery_dataset(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    location: str,
) -> None:
    """Create the BigQuery dataset if it does not already exist."""

    full_dataset_id = f"{project_id}.{dataset_id}"

    try:
        #try to get the dataset
        client.get_dataset(full_dataset_id)
        print(f"BigQuery dataset {full_dataset_id} already exists")

    except NotFound:
        #dataset not found, create it
        dataset = bigquery.Dataset(full_dataset_id)
        dataset.location = location
        client.create_dataset(dataset)
        print(f"Created BigQuery dataset {full_dataset_id}")


def validate_mysql_view_exists(engine: Engine, view_name: str) -> None:
    """Check whether the MySQL table/view exists before exporting."""
    sql = text(
        """
        SELECT COUNT(*) AS cnt
        FROM information_schema.views
        WHERE table_schema = :database_name
          AND table_name = :view_name
        """
    )

    database_name = get_required_env("MYSQL_DATABASE")

    with engine.connect() as conn:
        result = conn.execute(
            sql,
            {"database_name": database_name, "view_name": view_name},
        ).scalar()

    if result == 0:
        raise ValueError(
            f"MySQL view not found: {database_name}.{view_name}. "
            "Please check the view name."
        )

def export_view_to_bigquery(
    engine: Engine,
    bq_client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    view_name: str,
) -> None:
    print(f"Reading MySQL view: {view_name}")

    validate_mysql_view_exists(engine, view_name)

    query = f"SELECT * FROM `{view_name}`"
    df = pd.read_sql(query, engine)

    print(f"Rows read from MySQL: {len(df):,}")
    print(f"Columns: {list(df.columns)}")

    if df.empty:
        print(f"Warning: {view_name} is empty. Uploading an empty table may fail.")
        return

    table_id = f"{project_id}.{dataset_id}.{view_name}"

    # view tables already have data
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    print(f"Uploading to BigQuery table: {table_id}")

    load_job = bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )

    load_job.result()

    table = bq_client.get_table(table_id)

    print(f"Upload complete: {table_id}")
    print(f"BigQuery rows: {table.num_rows:,}")


def main() -> None:
    load_dotenv()

    project_id = get_required_env("GCP_PROJECT_ID")
    dataset_id = get_required_env("BQ_DATASET")
    location = os.getenv("BQ_LOCATION", "us-central1")

    print(f"GCP project: {project_id}")
    print(f"BigQuery dataset: {dataset_id}")
    print(f"BigQuery location: {location}")

    engine = create_mysql_engine()
    bq_client = bigquery.Client(project=project_id, location=location)

    ensure_bigquery_dataset(
        client=bq_client,
        project_id=project_id,
        dataset_id=dataset_id,
        location=location,
    )

    for view_name in VIEWS:
        export_view_to_bigquery(
            engine=engine,
            bq_client=bq_client,
            project_id=project_id,
            dataset_id=dataset_id,
            view_name=view_name,
        )

    print("=" * 80)
    print("All MySQL views have been exported to BigQuery successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Export failed.")
        print(f"Error: {error}")
        sys.exit(1)
    