# 從你的 task 檔案匯入剛剛寫好的函式
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo

# 主管手上的清單(pchome)
target_configs = [
    {'brand_name': 'Sony', 'search_q': 'Sony WH'},
    {'brand_name': 'Sennheiser', 'search_q': 'Sennheiser 降噪耳機'},
    {'brand_name': 'JLAB', 'search_q': 'JLAB 降噪耳機'},
    {'brand_name': 'Soundcore', 'search_q': 'Soundcore 降噪耳機'}
]

# 主管開始派單
for config in target_configs:
    pchome_brand = config['brand_name']
    pchome_keyword = config['search_q']
    
    print(f"發送任務到 RabbitMQ: 抓取 {pchome_brand}")
    
    # 使用 .delay() 將任務非同步丟給工人，並把參數傳進去
    crawler_pchome_print.delay(brand_name=pchome_brand, search_keyword=pchome_keyword)

print("派單完成！")


#momo

target_configs = [
    {'brand_name': 'Sony', 'search_q': 'Sony WH'},
    {'brand_name': 'Sennheiser', 'search_q': 'Sennheiser 降噪耳機'},
    {'brand_name': 'JLAB', 'search_q': 'JLAB 降噪耳機'},
    {'brand_name': 'Soundcore', 'search_q': 'Soundcore 降噪耳機'}
]


for config in target_configs:
    momo_brand_name = config['brand_name']
    momo_keywords = config['search_q']

    print(f"發送任務到 RabbitMQ: 抓取 {momo_brand_name}")

    scrape_momo.delay(brand_name= momo_brand_name , keywords = momo_keywords)

print("派單完成！")