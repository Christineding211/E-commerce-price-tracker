from airflow.providers.mysql.operators.mysql import MySqlOperator

def create_refresh_stg_pchome_task():

    return MySqlOperator(
        task_id="refresh_stg_pchome",
        mysql_conn_id="mysql_default",
        sql="etl/sql/refresh_stg_pchome.sql"
    )
  