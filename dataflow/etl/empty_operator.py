# 匯入 Airflow 中的 PythonOperator，可用來執行自定義的 Python 函式
from airflow.operators.python import (
    PythonOperator,
)


# 定義 crawler1 任務，會在 DAG 中顯示為 task_id = "crawler1"
# 執行時會輸出 "crawler1"
def create_crawler1_task() -> PythonOperator:
    return PythonOperator(
        # DAG 中的任務名稱
        task_id="crawler1",
        # 要執行的 Python 邏輯
        python_callable=lambda: print("crawler1"),
    )


# 定義 crawler2 任務，會輸出 "crawler2"
def create_crawler2_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler2",
        python_callable=lambda: print("crawler2"),
    )


# 定義 crawler3 任務，會輸出 "crawler3"
def create_crawler3_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler3",
        python_callable=lambda: print("crawler3"),
    )


# 定義 stock_strategy 任務，會輸出 "stock_strategy"
# 通常可以設計在爬完資料後進行分析或決策
def create_stock_strategy_task() -> PythonOperator:
    return PythonOperator(
        task_id="stock_strategy",
        python_callable=lambda: print("stock_strategy"),
    )
