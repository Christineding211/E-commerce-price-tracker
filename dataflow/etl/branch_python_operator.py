# 匯入 Airflow 所需的 Operators
from airflow.operators.empty import (
    EmptyOperator,
)  # 用於建立空的佔位任務（舊稱 DummyOperator）
from airflow.operators.python import (
    BranchPythonOperator,  # 用於條件分支邏輯
    PythonOperator,  # 用於執行 Python 函式
)


# 建立一個 EmptyOperator 任務，用於「跳過」的情境
def create_skip_task() -> EmptyOperator:
    return EmptyOperator(task_id="skip")


# 建立一個 PythonOperator 任務，用來執行爬蟲邏輯（這裡簡化為 print）
def create_crawler_task() -> PythonOperator:
    return PythonOperator(
        task_id="crawler",
        python_callable=lambda: print("crawler"),
    )


# 分支條件邏輯函式，會根據條件返回不同的 task_id
def check_crawler():
    # 檢查今天是否已經執行過爬蟲
    # 如果是，返回 "skip"（跳過爬蟲）
    # 否則返回 "crawler"（執行爬蟲）
    if True:
        return "skip"
    else:
        return "crawler"


# 建立 BranchPythonOperator 任務，決定流程接下來要走哪一個分支
def create_branch_python_operator_task():
    # 建立條件分支判斷任務
    check_crawler_task = BranchPythonOperator(
        task_id="CheckCrawler",
        python_callable=check_crawler,  # 執行條件函式
    )

    # 建立可能的兩個後續任務
    skip_task = create_skip_task()
    crawler_task = create_crawler_task()

    # 使用 `>>` 設定 DAG 執行順序（CheckCrawler 之後走 skip 或 crawler 任一）
    return check_crawler_task >> [
        skip_task,
        crawler_task,
    ]
