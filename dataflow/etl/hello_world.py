# 從 airflow 套件中匯入 PythonOperator（允許執行自定義的 Python 函數）
from airflow.operators.python import (
    PythonOperator,
)


def hello_world():
    print("hello_world")


# 定義一個建立 hello_world 任務的函數，回傳一個 PythonOperator 物件
def create_hello_world_task() -> PythonOperator:
    return PythonOperator(
        task_id="hello_world",  # 定義此 Task 在 DAG 中的唯一識別名稱
        python_callable=hello_world,  # 指定執行的 Python 函數
    )
