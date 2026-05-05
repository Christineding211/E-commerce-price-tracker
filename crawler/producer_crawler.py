# 從你的 task 檔案匯入剛剛寫好的函式

import time
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo
from crawler.worker import app # 導入 celery app 用來檢查狀態

# 1. 設定任務配置
target_configs = [
    {'brand': 'Sony', 'q': 'Sony WH'},
    {'brand': 'Sennheiser', 'q': 'Sennheiser 降噪耳機'},
    {'brand': 'JLAB', 'q': 'JLAB 降噪耳機'},
    {'brand': 'Soundcore', 'q': 'Soundcore 降噪耳機'}
]

print("開始壓力測試...")
start_time = time.time()

# 2. 正常派單 
for config in target_configs:
    crawler_pchome_print.delay(brand_name=config['brand'], search_keyword=config['q'])
    scrape_momo.delay(brand_name=config['brand'], keywords=config['q'])

print(f"📢 8 個任務已進入倉庫...")

# 3. 簡單計時邏輯：只要倉庫還有單，計時器就不停
while True:
    # 檢查現在還有多少任務在排隊 (active) 或 執行中 (reserved)
    inspect = app.control.inspect()
    active_tasks = inspect.active() or {}
    reserved_tasks = inspect.reserved() or {}
    
    # 計算所有 Worker 總共還剩下多少活沒幹完
    total_remaining = sum(len(tasks) for tasks in active_tasks.values()) + \
                      sum(len(tasks) for tasks in reserved_tasks.values())
    
    if total_remaining == 0:
        break # 沒單了，跳出迴圈
        
    print(f"⏳ 剩餘任務：{total_remaining} ... 繼續計時")
    time.sleep(2) # 每 2 秒檢查一次，

end_time = time.time()
print(f"\n✅ 測試完成！總執行耗時: {round(end_time - start_time, 2)} 秒")