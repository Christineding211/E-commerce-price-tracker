# 匯入 Airflow 核心模組
import airflow

# 匯入自定義的 DAG 設定常數
from dataflow.constant import (
    # 包含 DAG 的預設參數，例如 owner、start_date、retry 等
    DEFAULT_ARGS,
    # 同一時間允許同一 DAG 同時執行的最大次數
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 BranchPythonOperator 任務建構函式
from dataflow.etl.branch_python_operator import (
    # 回傳一組帶有條件分支邏輯的任務鏈
    create_branch_python_operator_task,
)

# 使用 with 語法建立 DAG 實例
with airflow.DAG(
    # DAG 的唯一識別名稱
    dag_id="BranchPythonOperator",
    # 套用預設的任務參數
    default_args=DEFAULT_ARGS,
    # 不定期排程，需手動或外部觸發
    schedule_interval=None,
    # 限制同一時間最多幾個執行中的 DAG run
    max_active_runs=MAX_ACTIVE_RUNS,
    # 不補跑過去未執行的 DAG run
    catchup=False,
) as dag:
    # 建立包含條件判斷邏輯的任務（如：是否執行爬蟲或跳過）
    create_branch_python_operator_task()
