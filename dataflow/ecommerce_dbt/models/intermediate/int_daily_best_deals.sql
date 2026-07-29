#dbt 裡通常會先建立一個 CTE

WITH daily_prices AS (

    SELECT *
    FROM {{ ref('stg_daily_prices') }}

),

unique_dates AS (
    SELECT DISTINCT scraped_date FROM daily_prices
),
unique_products AS (
    SELECT DISTINCT brand, official_model_name, platform FROM daily_prices
),
date_spine AS (
    SELECT d.scraped_date, p.brand, p.official_model_name, p.platform
    FROM unique_dates d
    CROSS JOIN unique_products p
),
raw_daily_min AS (
    SELECT 
        scraped_date, brand, official_model_name, platform,
        MIN(price) AS raw_min_price,
        -- 【改動地方 1】：先在這裡把當天的原始賣場數量算出來
        COUNT(original_code) AS raw_total_listings
    FROM daily_prices
    GROUP BY scraped_date, brand, official_model_name, platform
)
SELECT 
    s.scraped_date, s.brand, s.official_model_name, s.platform,
    
    -- 【改動地方 2】：在最外層把這個欄位撈出來。
    -- 這裡加一個 COALESCE(..., 0)，如果當天漏抓或沒賣（NULL），賣場數就自動歸 0
    COALESCE(r.raw_total_listings, 0) AS total_listings,

    -- 不管哪一天、不論什麼原因，只要是 NULL，就一律動態拿前一個有數值的價格來補
    LAST_VALUE(r.raw_min_price IGNORE NULLS) OVER (
        PARTITION BY s.brand, s.official_model_name, s.platform
        ORDER BY s.scraped_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS min_price
FROM date_spine s
-- 【改動地方 3】：因為上面是用 LEFT JOIN，r.raw_total_listings 會隨著 ON 條件自動對齊日期與商品接上來
LEFT JOIN raw_daily_min r 
    ON s.scraped_date = r.scraped_date 
    AND s.brand = r.brand 
    AND s.official_model_name = r.official_model_name 
    AND s.platform = r.platform;