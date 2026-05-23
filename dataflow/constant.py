import datetime  # 匯入 datetime 模組，用來設定時間參數

# 預設參數，會套用在 DAG 與 Task 中
DEFAULT_ARGS = {
    # DAG/Task 的負責人，顯示在 Airflow UI 中
    "owner": "Ecommerce",
    # 若任務失敗，最多重試 1 次
    "retries": 1,
    # 每次重試間隔 1 分鐘
    "retry_delay": datetime.timedelta(minutes=1),
    # DAG 開始生效的時間
    "start_date": datetime.datetime(2022, 1, 1),
    # 單一 task 最長可執行 60 分鐘，超時則視為失敗
    "execution_timeout": datetime.timedelta(minutes=60),
    # 限制 DAG 同時最多執行 10 個 task
    "concurrency": 10,
}

# 限制此 DAG 同時最多只能執行一個 run（防止排程或手動重疊執行）
MAX_ACTIVE_RUNS = 1
