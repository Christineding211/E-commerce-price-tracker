# 匯入 Airflow 主模組（用來定義 DAG）
import airflow

# 匯入 DAG 的預設參數與設定值
from dataflow.constant import (
    DEFAULT_ARGS,  # 預設參數，包含 start_date、retries、retry_delay 等
    MAX_ACTIVE_RUNS,  # 限制同時最多有幾個 DAG Run 在執行
)

# 匯入定義好的任務函式
from dataflow.etl.abcd import (
    create_a_task,  # 建立 task_a 的函式
    create_b_task,  # 建立 task_b 的函式
    create_c_task,  # 建立 task_c 的函式
    create_d_task,  # 建立 task_d 的函式
)

# 使用 DAG context manager 定義 DAG 名稱與屬性
with airflow.DAG(
    dag_id="ABCD",  # DAG 的唯一 ID
    default_args=DEFAULT_ARGS,  # 使用預設參數
    schedule_interval=None,  # 不定期排程（手動觸發）
    max_active_runs=MAX_ACTIVE_RUNS,  # 同時最多執行幾個 DAG Run
    catchup=False,  # 不補跑歷史的排程（start_date 以前的）
) as dag:
    # 建立 DAG 中的四個任務
    task_a = create_a_task()  # 印出 "a"
    task_b = create_b_task()  # 印出 "b"
    task_c = create_c_task()  # 印出 "c"
    task_d = create_d_task()  # 印出 "d"

    # 定義任務依賴關係：
    # task_a 先執行，然後同時觸發 task_b 與 task_c，
    # 等 b 和 c 都執行完之後再執行 task_d
    task_a >> [task_b, task_c] >> task_d
