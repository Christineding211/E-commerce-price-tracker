import os
from celery import Celery

# loguru 是比標準 logging 更好用的日誌套件, 不用繁瑣設定就能直接用
from loguru import logger

# 從 config.py 讀取 RabbitMQ 連線資訊
# RabbitMQ 是訊息中介 (message broker), Celery 透過它派送任務給 worker
from crawler.config import (
    RABBITMQ_HOST,  # RabbitMQ 主機位址, ex: localhost
    RABBITMQ_PORT,  # RabbitMQ 通訊埠, 預設 5672
    WORKER_ACCOUNT,  # 連線到 RabbitMQ 的帳號
    WORKER_PASSWORD,  # 連線到 RabbitMQ 的密碼
)

# 優先讀取環境變數中的 Broker URL (例如 Docker 中的 Redis)
# 如果沒有環境變數，才回退到 config 裡的 RabbitMQ 設定

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@rabbitmq:{RABBITMQ_PORT}/")
CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# 印出目前讀到的環境變數, 方便除錯確認設定是否正確載入
logger.info(f"""
    ========================================
    [Celery Environment Config Sync]
    - CELERY_BROKER_URL: {CELERY_BROKER}
    - CELERY_RESULT_BACKEND: {CELERY_BACKEND}
    ========================================
""")

# 建立 Celery app 實例, "task" 是這個應用程式的名稱
app = Celery(
    "task",
    # include: 告訴 Celery 要載入哪些 Python 模組裡的 task
    # 只有列在這裡的模組, 裡面用 @app.task 裝飾的函式才會被註冊為可執行任務
    include=[
        "crawler.task",  # 一般任務
        "crawler.tasks_crawler" #爬蟲任務
    ],
    # broker: 指定訊息中介的連線網址, Celery 會把任務送到這裡排隊
    # 格式: pyamqp://帳號:密碼@主機:埠號/
    # 例如: pyamqp://worker:worker@rabbitmq:5672/
    broker=CELERY_BROKER,       
    backend=CELERY_BACKEND
)
