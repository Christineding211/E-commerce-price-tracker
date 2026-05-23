# 從 Airflow 匯入 DockerOperator，用來在 DAG 中執行 Docker 容器任務
from airflow.providers.docker.operators.docker import (
    DockerOperator,
)


# 建立一個 DockerOperator 任務的函式，回傳一個 Airflow 的任務實例
def create_docker_operator_task() -> DockerOperator:
    return DockerOperator(
        # 設定這個 task 在 DAG 中的名稱（唯一識別碼）
        task_id="DockerOperator",
        # 指定要使用的 Docker 映像檔，例如 Ubuntu 22.04
        image="ubuntu:22.04",
        # 容器啟動後要執行的指令（這裡是輸出 hello world）
        command="echo hello world",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
    )
