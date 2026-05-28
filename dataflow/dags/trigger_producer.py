import airflow
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS
)
# 匯入新的單一平台派發函式
from dataflow.etl.trigger_producer import (
    run_single_producer_dispatch
)

# 假設以下任務的建立函式定義在 dataflow.etl 目錄下的不同模組中
# 例如：dataflow/etl/refresh_stg_momo.py 裡面有 create_refresh_stg_momo_task 函式
from dataflow.etl.refresh_stg_momo import create_refresh_stg_momo_task
from dataflow.etl.refresh_stg_pchome import create_refresh_stg_pchome_task
from dataflow.etl.refresh_fct_daily import create_refresh_fct_daily_task



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

    # 2. 拆開成兩個獨立的 Airflow 任務（看得清清楚楚！）
    trigger_momo_crawler = PythonOperator(
        task_id="trigger_momo_crawler",
        python_callable=run_single_producer_dispatch,
        op_kwargs={"platform": "momo", "queue_name": "momo_q"}
    )

    trigger_pchome_crawler = PythonOperator(
        task_id="trigger_pchome_crawler",
        python_callable=run_single_producer_dispatch,
        op_kwargs={"platform": "pchome", "queue_name": "pchome_q"}
    )

    # 3. 爬蟲完成後的 Empty Operator (用於標記爬蟲資料已準備好)
    crawlers_done_and_cleanup_marker = EmptyOperator(
        task_id="crawlers_done_and_cleanup"
    )

    # 4. Staging 任務 (PChome 和 Momo 的 Staging 可以並行執行)
    stg_momo_task = create_refresh_stg_momo_task()
    stg_pchome_task = create_refresh_stg_pchome_task()

    # 5. Fact Daily 任務
    fct_daily_task = create_refresh_fct_daily_task()

    # 定義任務依賴關係
    start_pipeline_marker >> [trigger_momo_crawler, trigger_pchome_crawler] >> crawlers_done_and_cleanup_marker
    crawlers_done_and_cleanup_marker >> [stg_momo_task, stg_pchome_task]
    [stg_momo_task, stg_pchome_task] >> fct_daily_task
