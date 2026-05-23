# 匯入 PythonOperator，這是 Airflow 中用來執行 Python 函式的 operator
from airflow.operators.python import (
    PythonOperator,
)


# 建立一個名為 a 的任務，執行時會印出 "a"
def create_a_task() -> PythonOperator:
    return PythonOperator(
        task_id="a",  # Task 的 ID（在 DAG 中需唯一）
        python_callable=lambda: print(
            "a"
        ),  # 指定要執行的函式，這裡是簡單的 lambda 表達式
    )


# 建立一個名為 b 的任務，執行時會印出 "b"
def create_b_task() -> PythonOperator:
    return PythonOperator(
        task_id="b",
        python_callable=lambda: print("b"),
    )


# 建立一個名為 c 的任務，執行時會印出 "c"
def create_c_task() -> PythonOperator:
    return PythonOperator(
        task_id="c",
        python_callable=lambda: print("c"),
    )


# 建立一個名為 d 的任務，執行時會印出 "d"
def create_d_task() -> PythonOperator:
    return PythonOperator(
        task_id="d",
        python_callable=lambda: print("d"),
    )
