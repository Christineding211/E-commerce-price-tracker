from airflow.providers.mysql.operators.mysql import MySqlOperator

def create_refresh_stg_momo_task():

    return MySqlOperator(
        task_id="refresh_stg_momo",
        mysql_conn_id="mysql_default",
        sql="etl/sql/refresh_stg_momo.sql"
    )
