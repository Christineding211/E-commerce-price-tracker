import time
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo
from crawler.worker import app


def run_multi_queue_test():
    target_configs = [
        {'brand': 'Sony', 'q': 'Sony WH'},
        {'brand': 'Sennheiser', 'q': 'Sennheiser 降噪耳機'},
        {'brand': 'JLAB', 'q': 'JLAB 降噪耳機'},
        {'brand': 'Soundcore', 'q': 'Soundcore 降噪耳機'}
    ]
# .s() = signature, 將 task 和參數「綁定」成一個可派送的物件
# 這樣就能更彈性地指定 queue
#apply_async 下單派出去
    start_time = time.time()
    for config in target_configs:
        #pchome通道
        crawler_pchome_print.s(brand_name = config['brand'], search_keyword = config['q']).apply_async(queue="pchome_q")
        #momo 通道
        scrape_momo.s(brand_name = config['brand'], keywords = config['q']).apply_async(queue = 'momo_q')
    
    print("任務已全數派發")

    while True:
        #查看目前情況
        inspect = app.control.inspect()
        #目前正在做的任務數，沒有抓到就給{}
        active = inspect.active()or {}
        #統計哪些單子是已經領走，但還排隊等著做的？
        #reserved 代表任務已經被 Worker 領走放在預約清單裡，但還沒開始爬。
        reserved = inspect.reserved() or {}

        # 計算所有 Worker 總共還剩下多少活沒幹完
        total = sum(len(t) for t in active.values()) + sum(len(t) for t in reserved.values())

        if total == 0:
            break

        print(f"剩餘任務：{total}")
        time.sleep(2)

    end_time = time.time()
    print(f"分流架構總耗時: {round(end_time - start_time, 2)} 秒")

if __name__ == "__main__":
    run_multi_queue_test()
