import time
from airflow.operators.python import PythonOperator

# 匯入外部的爬蟲 Task 與 Celery App
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo
from crawler.worker import app

def run_single_producer_dispatch(platform: str, queue_name: str):
    """
    根據平台派發任務，並等待該 Queue 中的所有任務執行完畢。
    """
    target_configs = [
        {'brand': 'Sony', 'q': 'Sony WH'},
        {'brand': 'Sennheiser', 'q': 'Sennheiser 降噪耳機'},
        {'brand': 'JLAB', 'q': 'JLAB 降噪耳機'},
        {'brand': 'Soundcore', 'q': 'Soundcore 降噪耳機'}
    ]

    print(f"Airflow is launching the {platform} crawler dispatcher to queue: {queue_name}")
    
    for config in target_configs:
        if platform == "pchome":
            crawler_pchome_print.s(
                brand_name=config['brand'], 
                search_keyword=config['q']
            ).apply_async(queue=queue_name)
        elif platform == "momo":
            scrape_momo.s(
                brand_name=config['brand'], 
                keywords=config['q']
            ).apply_async(queue=queue_name)
    
    print(f"Tasks for {platform} successfully dispatched. Waiting for completion...")

    # 監控邏輯：只檢查屬於目前 queue_name 的任務
    while True:
        inspect = app.control.inspect()
        active = inspect.active() or {}
        reserved = inspect.reserved() or {}

        total_remaining = 0
        # 檢查所有 Worker 身上正在執行 (active) 或 預約 (reserved) 的任務
        for worker_tasks in active.values():
            total_remaining += sum(1 for t in worker_tasks if t.get('delivery_info', {}).get('routing_key') == queue_name)
        for worker_tasks in reserved.values():
            total_remaining += sum(1 for t in worker_tasks if t.get('delivery_info', {}).get('routing_key') == queue_name)

        if total_remaining == 0:
            print(f"All {platform} tasks in queue {queue_name} completed.")
            break

        print(f"Remaining {platform} tasks: {total_remaining}. Waiting 10s...")
        time.sleep(10)
