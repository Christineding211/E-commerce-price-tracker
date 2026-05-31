
# 目前方法 A 不使用，保留作為舊版 Celery crawler 架構參考。

# 確保這裡的 app 連線地址已經改為 'rabbitmq'
from crawler.worker import app


def dispatch_tasks():
    target_configs = [
        {'brand': 'Sony', 'q': 'Sony WH'},
        {'brand': 'Sennheiser', 'q': 'Sennheiser 降噪耳機'},
        {'brand': 'JLAB', 'q': 'JLAB 降噪耳機'},
        {'brand': 'Soundcore', 'q': 'Soundcore 降噪耳機'}
    ]

    print("Starting to dispatch tasks to queue")
    
    for config in target_configs:
        # 派發到 PChome 隊列
        crawler_pchome_print.s(
            brand_name=config['brand'], 
            search_keyword=config['q']
        ).apply_async(queue="pchome_q")
        
        # 派發到 Momo 隊列
        scrape_momo.s(
            brand_name=config['brand'], 
            keywords=config['q']
        ).apply_async(queue='momo_q')
    
    print("All tasks have been successfully dispatched to the RabbitMQ queue!")
    

if __name__ == "__main__":
    dispatch_tasks()
