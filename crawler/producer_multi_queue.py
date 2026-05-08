
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo
# 確保這裡的 app 連線地址已經改為 'rabbitmq'
from crawler.worker import app


def dispatch_tasks():
    target_configs = [
        {'brand': 'Sony', 'q': 'Sony WH'},
        {'brand': 'Sennheiser', 'q': 'Sennheiser 降噪耳機'},
        {'brand': 'JLAB', 'q': 'JLAB 降噪耳機'},
        {'brand': 'Soundcore', 'q': 'Soundcore 降噪耳機'}
    ]

    print("開始派發任務到內網倉庫...")
    
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
    
    print("任務已全數成功進入 RabbitMQ 倉庫！")
    

if __name__ == "__main__":
    dispatch_tasks()
