from airflow.providers.mysql.operators.mysql import MySqlOperator

def create_refresh_fct_daily_task():
    return MySqlOperator(
        task_id="refresh_fct_daily",
        mysql_conn_id="mysql_default",
        sql="etl/sql/refresh_fct_daily.sql"
    )

