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
calculated_price_diff as (

    select
        scraped_date,
        brand,
        official_model_name,
        momo_price,
        pchome_price,
        momo_price - pchome_price as price_diff
    from bundled_prices

)
-- 使用 SAFE_DIVIDE ，預防 PChome 缺貨變 0 導致管線崩潰
select
    scraped_date,
    brand,
    official_model_name,
    momo_price,
    pchome_price,
    price_diff,
    round(
        safe_divide(price_diff, pchome_price) * 100,
        2
    ) as price_diff_pct
from calculated_price_diff
