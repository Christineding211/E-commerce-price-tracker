# 匯入 PythonOperator，用於在 DAG 中執行 Python 函式
from airflow.operators.python import (
    PythonOperator,
)
from dataflow.crawler.tasks_crawler import scrape_momo

# 定義一個簡單的 Python 函式，作為任務執行內容
def crawler():
    print("crawler")  # 執行任務時會輸出 "crawler"


# 建立一個 PythonOperator 任務，將上述 crawler 函式包裝成 DAG 中的一個任務
def create_python_operator_task() -> PythonOperator:
    return PythonOperator(
        # DAG 中的任務 ID，需唯一
        task_id="PythonOperator",
        # 指定要執行的 Python 函式
        python_callable=crawler,
    )


def scrape_momo_task() -> PythonOperator:
    return PythonOperator(
        # DAG 中的任務 ID，需唯一
        task_id="PythonOperator",
        # 指定要執行的 Python 函式
        python_callable= scrape_momo,
    )
