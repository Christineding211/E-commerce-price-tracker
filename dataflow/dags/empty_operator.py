# 匯入 Airflow 主模組與 EmptyOperator（用於建立空白佔位任務，舊稱 DummyOperator）
import airflow
from airflow.operators.empty import (
    EmptyOperator,
)

# 匯入自定義的常數設定（包含預設參數與最大同時運行數）
from dataflow.constant import (
    DEFAULT_ARGS,
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 EmptyOperator 任務建構函式
from dataflow.etl.empty_operator import (
    create_crawler1_task,  # 爬蟲任務1
    create_crawler2_task,  # 爬蟲任務2
    create_crawler3_task,  # 爬蟲任務3
    create_stock_strategy_task,  # 股票策略任務
)

# 定義 DAG，並使用 with 語法進入 DAG 環境
with airflow.DAG(
    # DAG 的唯一識別名稱
    dag_id="EmptyOperator",
    # 套用預設參數
    default_args=DEFAULT_ARGS,
    # 無排程，手動或外部觸發
    schedule_interval=None,
    # 限制同時間最多執行的 DAG 數量
    max_active_runs=MAX_ACTIVE_RUNS,
    # 禁止補跑過去未執行的排程
    catchup=False,
) as dag:
    # 建立一個總爬蟲任務 EmptyOperator，作為起點
    crawler_task = EmptyOperator(task_id="crawler_task")

    # 建立一個策略任務 EmptyOperator，作為爬蟲任務之後的彙整點
    strategy_task = EmptyOperator(task_id="strategy_task")

    # 定義任務依賴關係：
    # crawler_task 先執行，之後同時觸發三個 crawler 任務（crawler1、crawler2、crawler3）
    # 三個 crawler 任務全部完成後，再執行 strategy_task
    # strategy_task 完成後，執行最終的股票策略任務 create_stock_strategy_task()
    (
        crawler_task
        >> [
            create_crawler1_task(),
            create_crawler2_task(),
            create_crawler3_task(),
        ]
        >> strategy_task
        >> create_stock_strategy_task()
    )
