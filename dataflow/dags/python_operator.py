# 匯入 Airflow 的主模組
import airflow

# 匯入自定義的常數設定
from dataflow.constant import (
    # 預設參數，例如 start_date、retries、owner 等
    DEFAULT_ARGS,
    # 限制同一時間最多可同時執行的 DAG run 數量
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 PythonOperator 任務建立函式
from dataflow.etl.python_operator import (
    # 回傳一個 PythonOperator 任務的函式
    create_python_operator_task,
)

# 定義 DAG 本體，使用 with 語法建立 DAG 物件與其任務內容
with airflow.DAG(
    # DAG 的唯一 ID，建議用有意義的名稱
    dag_id="PythonOperator",
    # 套用預設設定（可設定重試次數、延遲時間等）
    default_args=DEFAULT_ARGS,
    # 不設定排程，代表需要手動或外部觸發
    schedule_interval=None,
    # 限制同時執行的 DAG run 數，避免重複執行
    max_active_runs=MAX_ACTIVE_RUNS,
    # 禁止補跑過去尚未執行的排程（推薦在手動觸發場景）
    catchup=False,
) as dag:
    # 建立 PythonOperator 任務，並註冊到 DAG 中
    create_python_operator_task()
