
SELECT 
    scraped_date,
    brand,
    official_model_name,
    platform,
    total_listings, 
    today_price,
    yesterday_price,
    history_all_time_low,
    ROUND(SAFE_DIVIDE((yesterday_price - today_price), yesterday_price) * 100, 2) AS price_drop_pct
FROM {{ ref('mart_product_price_timeline') }}
WHERE today_price <= history_all_time_low
  AND yesterday_price IS NOT NULL