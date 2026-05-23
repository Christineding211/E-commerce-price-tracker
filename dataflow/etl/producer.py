# 從 Airflow 匯入 DockerOperator，用來在 DAG 中執行 Docker 容器任務
from airflow.providers.docker.operators.docker import (
    DockerOperator,
)


# 建立一個 DockerOperator 任務的函式，回傳一個 Airflow 的任務實例
def create_producer_task() -> DockerOperator:
    return DockerOperator(
        # 設定這個 task 在 DAG 中的名稱（唯一識別碼）
        task_id="producer_crawler_finmind_duplicate",
        image="linsamtw/tibame_crawler:0.0.6",
        command="uv run --env-file=.env python -m crawler.producer_crawler_finmind_duplicate",
        # 每次執行前都強制重新拉取最新的 image（確保使用最新版本）
        force_pull=True,
        # 容器執行完畢後自動刪除（避免堆積殘留容器）
        auto_remove=True,
        # ✅ 指定容器要使用的 Docker network 名稱
        # 注意：這要是 Docker Engine 中已存在的 network 名稱
        network_mode="my_attachable_network",
    )
