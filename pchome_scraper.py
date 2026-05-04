import requests
import pandas as pd
# import bs4 as bs
import json
from datetime import datetime
import time
from sqlalchemy import create_engine, text



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'content-type': 'application/json'
}


# 基礎 URL 保持乾淨
url = 'https://ecshweb.pchome.com.tw/search/v4.3/all/results'

# 改動 1重新定義目標：用「關鍵字」取代「品牌 ID」

target_configs = [
    {'brand_name': 'Sony', 'search_q': 'Sony WH'},
    {'brand_name': 'Sennheiser', 'search_q': 'Sennheiser 降噪耳機'},
    {'brand_name': 'JLAB', 'search_q': 'JLAB 降噪耳機'},
    {'brand_name': 'Soundcore', 'search_q': 'Soundcore 降噪耳機'}
]
# 改動 2定義通用的降噪功能 ID
NOISE_CANCEL_ATTR = "G25I21304"

total_result = []

for config in target_configs:
    brand_name = config['brand_name']
    search_keyword = config['search_q']

    print(f"processing {brand_name}, search keyword:{search_keyword}")

    params = {
        'q': search_keyword,      
        'attr': NOISE_CANCEL_ATTR, # 改動 4統一使用降噪功能標籤，不再分品牌 ID
        'price': "2000-9000",
        'page': 1,
        'pageCount': 40
    }
    try:
        resp = requests.get(url, headers=headers, params=params)
        # 加上保險：如果請求失敗直接跳過
        if resp.status_code != 200:
            print(f"警告：{brand_name} 請求失敗，狀態碼：{resp.status_code}")
            continue

        first_res = resp.json()
        total_page = first_res.get("TotalPage", 1)
        print(f"Total page: {total_page}")

        # 2. 開始分頁爬取
        for page in range(1, total_page + 1):
            params['page'] = page
            data = requests.get(url, headers=headers, params=params).json()
            products = data.get('Prods', [])

            #有時候 PChome 的 TotalPage 會給比較多，但後面其實沒貨。加一個檢查，沒資料就提早結束這個品牌的 Loop，省時間。
            if not products:
                print(f"第 {page} 頁沒有商品，結束此品牌抓取。")
                break

            for product in products:
                name_tag = product.get('Name', '未知').strip()
                id_tag = product.get('Id', '')
                price_tag = product.get('Price', 0)

                # 取得評分，若無則預設為 0
                raw_rating = product.get('ratingValue', 0)
                try:
                    rating_tag = float(raw_rating) if raw_rating else 0.0
                except (ValueError, TypeError):
                    rating_tag = 0.0

                row = {
                    'Brand': brand_name,
                    'Name': name_tag,
                    'ID': id_tag,
                    'Price': int(price_tag),
                    'Rating': rating_tag,
                    'Source': 'PChome', # 增加來源標記，以後進庫好區分
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                total_result.append(row)
            print(f"第{page} 頁抓取完，目前累計 {len(total_result)} 筆商品")
            time.sleep(1)

    except Exception as e:
        print(f"正在抓取{brand_name} 時發生問題",e)

print(f"\n--- 抓取結束，總共獲得 {len(total_result)} 筆資料 ---")
