# 匯入 Airflow 核心模組
import airflow

# 匯入自定義的常數設定，用於統一管理 DAG 參數與執行限制
from dataflow.constant import (
    # 預設參數，例如 owner、start_date、retries 等
    DEFAULT_ARGS,
    # 限制同一時間同一 DAG 最多允許幾個執行實例
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 DockerOperator 任務建立函式
from dataflow.etl.producer_twse import (
    # 建立並回傳一個 DockerOperator 任務
    create_producer_twse_task,
)

# 定義 DAG，並用 with 語法將任務放入 DAG 環境中
with airflow.DAG(
    # DAG 的唯一名稱，用來識別 DAG
    dag_id="ProducerTwse",
    # 套用預設參數設定
    default_args=DEFAULT_ARGS,
    # 不自動排程，只能手動或外部觸發
    schedule_interval=None,
    # 限制同時執行的最大 DAG 實例數
    max_active_runs=MAX_ACTIVE_RUNS,
    # 禁止補跑過去未執行的排程
    catchup=False,
) as dag:
    # 建立並註冊 DockerOperator 任務到 DAG
    create_producer_twse_task()
