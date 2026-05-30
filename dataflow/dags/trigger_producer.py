import airflow
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS
)


# 假設以下任務的建立函式定義在 dataflow.etl 目錄下的不同模組中
# 例如：dataflow/etl/refresh_stg_momo.py 裡面有 create_refresh_stg_momo_task 函式
from dataflow.etl.refresh_stg_momo import create_refresh_stg_momo_task
from dataflow.etl.refresh_stg_pchome import create_refresh_stg_pchome_task
from dataflow.etl.refresh_fct_daily import create_refresh_fct_daily_task
from dataflow.etl.trigger_producer import create_scraper_tasks




with airflow.DAG(
    
    dag_id="E-commerce_prices_pipeline",

    default_args=DEFAULT_ARGS,
    
    schedule_interval=None,
    
    max_active_runs=MAX_ACTIVE_RUNS,
    
    catchup=False,

    # 告訴 Airflow 去容器內的這裡找 SQL(docker container)
    template_searchpath=["/dataflow/dataflow"]
) as dag:
    
    # 1. 起始 Empty Operator，表示整個 ETL 流程的開始
    start_pipeline_marker = EmptyOperator(
        task_id="start_pipeline"
    )

    pchome_tasks, momo_tasks = create_scraper_tasks()
    all_crawler_tasks = pchome_tasks + momo_tasks


    # 3. 爬蟲完成後的 Empty Operator (用於標記爬蟲資料已準備好)
    crawlers_done_marker = EmptyOperator(
        task_id="crawlers_done"
    )

    # 4. Staging 任務 (PChome 和 Momo 的 Staging 可以並行執行)
    stg_momo_task = create_refresh_stg_momo_task()
    stg_pchome_task = create_refresh_stg_pchome_task()

    # 5. Fact Daily 任務
    fct_daily_task = create_refresh_fct_daily_task()

    # 定義任務依賴關係
    start_pipeline_marker >> all_crawler_tasks
    all_crawler_tasks >> crawlers_done_marker

    crawlers_done_marker >> [stg_momo_task, stg_pchome_task]
    [stg_momo_task, stg_pchome_task] >> fct_daily_task
