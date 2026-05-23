# 從 Airflow 的 operators 模組中引入 BashOperator，用於執行 Bash 指令
from airflow.operators.bash import (
    BashOperator,
)


# 定義一個函數 create_bash_operator_task，回傳一個 BashOperator 物件
def create_bash_operator_task() -> BashOperator:
    return BashOperator(
        # 指定該 task 的 ID，DAG 中的唯一識別名稱
        task_id="BashOperator",
        # 要在 shell 中執行的指令，這裡是輸出一段文字
        bash_command="echo BashOperator",
    )
