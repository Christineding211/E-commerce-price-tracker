# 匯入 airflow 模組（主要是為了使用 airflow.DAG）
import airflow

# 從自定義模組 dataflow.constant 匯入 DAG 的預設參數與最大執行數
from dataflow.constant import (
    DEFAULT_ARGS,  # 預設參數，通常會定義 start_date、owner、retries 等
    MAX_ACTIVE_RUNS,  # 此 DAG 同時間最多允許幾個執行實例（通常設為 1 或 3）
)

# 從自定義的 ETL 模組匯入任務建構函數
from dataflow.etl.hello_world import (
    create_hello_world_task,  # 建立 hello_world 任務的函數
)

# 使用 DAG context manager 定義一個 DAG
with airflow.DAG(
    dag_id="HelloWorld",  # DAG 的唯一識別 ID
    default_args=DEFAULT_ARGS,  # 套用預設參數（建議從 constant 統一管理）
    schedule_interval=None,  # 不排程（手動觸發），可改為 '0 8 * * *' 等排程字串
    max_active_runs=MAX_ACTIVE_RUNS,  # 同時間最多允許幾個 DAG Run 執行
    catchup=False,  # 不補跑歷史排程（通常設為 False）
) as dag:
    # 加入 hello_world 任務
    create_hello_world_task()  # 回傳的 PythonOperator 會自動註冊到 DAG 內
