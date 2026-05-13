import pandas as pd
import requests
import time
from datetime import datetime
from crawler.worker import app # 記得匯入 Celery app
from sqlalchemy import create_engine  # 建立資料庫連線的工具（SQLAlchemy）
from datetime import datetime, timedelta, timezone


from crawler.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT


# 加上裝飾器，讓它變成可派送的任務
@app.task()
def crawler_pchome_print(brand_name, search_keyword):
    print(f"--- 工人開始執行任務: 尋找 {brand_name} ---")
    # brand_name = 'Sony'
    # search_keyword = 'Sony WH'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'content-type': 'application/json'
    }
    url = 'https://ecshweb.pchome.com.tw/search/v4.3/all/results'

    
    NOISE_CANCEL_ATTR = "G25I21304"

    
    # 注意：這個 total_result 必須放在函式裡面！
    # 這樣每個工人 (每個 Task) 才會擁有自己獨立的清單，不會跟別人打架
    total_result = []

    params = {
        'q': search_keyword,
        'attr': NOISE_CANCEL_ATTR,
        'price': "2000-9000",
        'page': 1,
        'pageCount': 40
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            error_msg = f"❌ 請求失敗 {brand_name}, 代碼: {resp.status_code}"
            print(error_msg)
            return error_msg  #在 Flower 的結果欄位會看到這串字

        first_res = resp.json()
        total_page = first_res.get("TotalPage", 1)
        print(f"{brand_name} 總共有 {total_page} 頁")

        # 開始分頁爬取
        for page in range(1, total_page + 1):
            params['page'] = page
            data = requests.get(url, headers=headers, params=params).json()
            products = data.get('Prods', [])

            if not products:
                print(f"第 {page} 頁沒有商品，結束 {brand_name} 抓取。")
                break

            for product in products:
                name_tag = product.get('Name', '未知').strip()
                id_tag = product.get('Id', '')
                price_tag = product.get('Price', 0)
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
                    'Source': 'PChome',
                    'scraped_at': datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
                }
                total_result.append(row)
                
            print(f"{brand_name} 第 {page} 頁抓取完，累計 {len(total_result)} 筆商品")
            time.sleep(1) 

        # 轉成 DataFrame 
        df = pd.DataFrame(total_result)

        if not df.empty:
            print(f"\n {brand_name}結束，共獲取 {len(df)} 筆資料")

            upload_data_to_mysql(df, "stg_pchome_prices")
            return f"{brand_name} success and uploaded"
        else:
            print(f" {brand_name} 沒有抓到資料")
            return f"{brand_name} no data"

    except Exception as e:
        print(f"正在抓取 {brand_name} 時發生問題: {e}")
        return "Error"


@app.task()
def scrape_momo(brand_name, keywords):
    #{'brand': 'Sony', 'q': 'Sony WH'},
    # brand_name = 'Sony'
    # keywords = 'Sony WH'
    url = 'https://apisearch.momoshop.com.tw/momoSearchCloud/moec/textSearch'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        'content-type': 'application/json'
    }

    print(f"processing {brand_name}, search keyword:{keywords}")

    task_results = []

    payload = {
        "host": "ecmobile",
        "flag": "searchEngine",
        "data": {
            "searchValue": keywords,
            "priceS": "2000",
            "priceE": "9000",
            "curPage": 1
        }
    }

    try:
        first_res = requests.post(url, headers = headers, json = payload)
        if first_res.status_code != 200:
            error_msg = f"❌ 請求失敗 {brand_name}, 代碼: {first_res.status_code}"
            print(error_msg)
            return error_msg  #在 Flower 的結果欄位會看到這串字
        
        first_res=  first_res.json()
        total_page = first_res.get('maxPage',1)
        

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
                    'SalesInfo':sales_tag,
                    'Source': 'momo',
                    'scraped_at': datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
                  }
                task_results.append(row)
            print(f"第{page} 頁抓取完，目前累計 {len(task_results)} 筆商品")
            time.sleep(4) # momo 比較嚴格，間隔時間長一點

        
        df = pd.DataFrame(task_results)
        
        if not df.empty:
            print(f"\n {brand_name}結束，共獲取 {len(df)} 筆資料")

            upload_data_to_mysql(df, "stg_momo_prices")
            return f"{brand_name} success and uploaded"
        else:
            print(f" {brand_name} 沒有抓到資料")
            return f"{brand_name} no data"

    except Exception as e:
        print(f"正在抓取{brand_name} 時發生問題",e)




def upload_data_to_mysql(df: pd.DataFrame, table_name: str):
    # 定義資料庫連線字串（MySQL 資料庫）
    # 格式：mysql+pymysql://使用者:密碼@主機:port/資料庫名稱
    # 上傳到 mydb, 同學可切換成自己的 database
    try:
        address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/headphone_db"

        # 建立 SQLAlchemy 引擎物件

        engine = create_engine(address)

        df.to_sql(
            name = table_name,
            con=engine,
            if_exists="append",
            index=False,
        )
        print(f"成功寫入 {len(df)} 筆資料至 {table_name}")
    except Exception as e:
        print("fail to upload to db", e)