# 匯入 Airflow 核心模組
import airflow

# 匯入自定義的常數設定，例如預設參數與同時執行的最大 DAG 次數
from dataflow.constant import (
    # 預設的 DAG 任務參數（如 owner、start_date 等）
    DEFAULT_ARGS,
    # 允許同時執行的最大 DAG 次數
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 BashOperator 建立函式（來自你自己寫的模組）
from dataflow.etl.bash_operator import (
    create_bash_operator_task,
)

# 使用 `with` 語法建立一個 DAG 實例，並將其命名為 "BashOperator"
with airflow.DAG(
    # DAG 的唯一識別名稱
    dag_id="BashOperator",
    # 套用預設參數設定（包含 start_date、retries 等）
    default_args=DEFAULT_ARGS,
    # 不排程，自動化工具或手動觸發（None 表示僅限手動）
    schedule_interval=None,
    # 同時間最多允許幾個執行中的 DAG run
    max_active_runs=MAX_ACTIVE_RUNS,
    # 不補跑過去未執行的 DAG run（False 為推薦值）
    catchup=False,
) as dag:
    # 建立一個 BashOperator 任務並加入 DAG 中
    create_bash_operator_task()
