
WITH base AS (
    -- 1. 從中間層把 min_price 新加的 total_listings 
    SELECT 
        scraped_date,
        brand,
        official_model_name,
        platform,
        total_listings, 
        min_price AS today_price
    FROM {{ ref('int_daily_best_deals') }}
),
calculated_timeline AS (
    -- 2. 計算昨天價格與歷史最低價（縱向時間軸視窗函數）
    SELECT
        scraped_date,
        brand,
        official_model_name,
        platform,
        total_listings,
        today_price,
        LAG(today_price) OVER (
            PARTITION BY brand, official_model_name, platform 
            ORDER BY scraped_date
        ) AS yesterday_price,
        MIN(today_price) OVER (
            PARTITION BY brand, official_model_name, platform 
            ORDER BY scraped_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS history_all_time_low
    FROM base
)
-- 3. 在最外層，price_buffer 百分比算出來
SELECT 
    scraped_date,
    brand,
    official_model_name,
    platform,
    total_listings,
    today_price,
    yesterday_price,
    history_all_time_low,
    -- 當今天價格等於歷史最低
    ROUND(SAFE_DIVIDE((today_price - history_all_time_low), today_price) * 100, 2) AS price_buffer
FROM calculated_timeline