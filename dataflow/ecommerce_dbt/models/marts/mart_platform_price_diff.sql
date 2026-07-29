WITH bundled_prices AS (
    SELECT 
        scraped_date,
        brand,
        official_model_name,
        MAX(CASE WHEN platform = 'momo' THEN min_price END) AS momo_price,
        MAX(CASE WHEN platform = 'pchome' THEN min_price END) AS pchome_price
    FROM {{ ref('int_daily_best_deals') }}
    GROUP BY scraped_date, brand, official_model_name
),
price_diff AS (

    SELECT
        scraped_date,
        brand,
        official_model_name,
        momo_price,
        pchome_price,
        momo_price - pchome_price AS price_diff
    FROM bundled_prices
)
-- 使用 SAFE_DIVIDE ，預防 PChome 缺貨變 0 導致管線崩潰
SELECT
    *,
    ROUND(
        SAFE_DIVIDE(price_diff, pchome_price) * 100,
        2
    ) AS price_diff_pct
FROM price_diff
