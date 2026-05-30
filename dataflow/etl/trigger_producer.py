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
    time.sleep(3) #airflow palse for 3

    # 監控邏輯：只檢查屬於目前 queue_name 的任務
    while True:
        inspect = app.control.inspect()
        
        # 🎯 核心修正 2：防禦性程式碼（避免 inspect 連線不到時直接崩潰）
        if not inspect:
            print("⚠️ [Airflow] 無法連線到 Celery Broker / Worker，10 秒後重試...")
            time.sleep(10)
            continue

        # 確保即使 Worker 沒反應，拿到的也是字典，不會變成 None
        active = inspect.active() or {}
        reserved = inspect.reserved() or {}

        total_remaining = 0
        
        # 檢查所有 Worker 身上正在執行 (active) 的任務
        for worker_tasks in active.values():
            # 這裡多加一個 if worker_tasks，確保裡面有東西才算
            if worker_tasks:
                total_remaining += sum(1 for t in worker_tasks if t.get('delivery_info', {}).get('routing_key') == queue_name)
                
        # 檢查所有 Worker 預約 (reserved) 的任務
        for worker_tasks in reserved.values():
            if worker_tasks:
                total_remaining += sum(1 for t in worker_tasks if t.get('delivery_info', {}).get('routing_key') == queue_name)

        # 🎯 經過 3 秒緩衝後，如果這時候算出來真的歸零了，才是真正的「打怪結束」
        if total_remaining == 0:
            print(f"🎉 [Airflow] All {platform} tasks in queue {queue_name} completed.")
            break

        print(f"⏳ [Airflow] Remaining {platform} tasks: {total_remaining}. Waiting 10s...")
        time.sleep(10)
