import requests
# import pandas as pd
# import bs4 as bs
import json
from datetime import datetime
import time
from sqlalchemy import create_engine, text



url = 'https://apisearch.momoshop.com.tw/momoSearchCloud/moec/textSearch'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'content-type': 'application/json'
}

target_configs = [
    {'brand_name': 'Sony', 'search_q': 'Sony WH'},
    {'brand_name': 'Sennheiser', 'search_q': 'Sennheiser 降噪耳機'},
    {'brand_name': 'JLAB', 'search_q': 'JLAB 降噪耳機'},
    {'brand_name': 'Soundcore', 'search_q': 'Soundcore 降噪耳機'}
]

result = []

for config in target_configs:
    brand_name = config['brand_name']
    keywords = config['search_q']

    print(f"processing {brand_name}, search keyword:{keywords}")


    min_price = "2000"
    max_price = "9000"
    current_page = "1"

    payload = {
        "host":"ecmobile",
        "flag":"searchEngine",
        "data":{
           "searchValue": keywords,
            "priceS": min_price,
            "priceE": max_price,
            "curPage":1
        }
    }
    try:
        first_res = requests.post(url, headers = headers, json = payload)
        if first_res.status_code != 200:
            print(f"請求失敗{brand_name}, status_code :{first_res.status_code}")
            continue
        first_res=  first_res.json()
        total_page = first_res.get('maxPage',1)
        print(f"Total page: {total_page}")

        for page in range(1, total_page + 1):
            payload['data']['curPage'] = page
            response = requests.post(url, headers = headers, json = payload).json()

            product = response.get('rtnSearchData', {}).get('goodsInfoList',[])
            for item in product:
                name_tag = item.get('goodsName','未知').strip()
                id_tag = item.get('goodsCode','')
                clean_price = item.get('goodsPriceModel',{}).get('basePrice',{}).get('price', 0)
                price_tag = str(clean_price).replace(',','')
                sales_tag = item.get('totalSalesInfo',{}).get('text', '').strip()
                raw_rating = item.get('rating','0')
                try:
                    rating_tag = float(raw_rating) if raw_rating else 0.0
                except ValueError:
                    rating_tag = 0.0

                row = {
                    'Brand': brand_name,
                    'Name': name_tag,
                    'ID': id_tag,
                    'Price': int(price_tag),
                    'Rating': rating_tag,
                    'SalseInfo':sales_tag,
                    'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  }
                result.append(row)
            print(f"第{page} 頁抓取完，目前累計 {len(result)} 筆商品")
            time.sleep(1)

    except Exception as e:
        print(f"正在抓取{brand_name} 時發生問題",e)


print(f"\n--- 抓取結束，總共獲得 {len(result)} 筆資料 ---")
