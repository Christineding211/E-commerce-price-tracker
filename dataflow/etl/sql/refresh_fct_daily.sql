

DELETE FROM fct_daily_prices 
WHERE scraped_date = '{{ ds }}';

-- 2. 天天執行的增量精準比對
INSERT INTO fct_daily_prices (scraped_date, brand, official_model_name, platform, original_code, price)
SELECT scraped_date, brand, official_model_name, platform, original_code, price
FROM (
    SELECT 
        momo.scraped_date, dim.brand, dim.official_model_name, 'momo' AS platform, momo.ID AS original_code, momo.Price AS price,
        ROW_NUMBER() OVER(PARTITION BY momo.ID, momo.scraped_date ORDER BY LENGTH(dim.keyword) DESC) AS rank_id
    FROM stg_momo_prices momo
    JOIN dim_products dim ON LOWER(momo.Name) LIKE CONCAT('%', dim.keyword, '%')
    WHERE momo.scraped_date = '{{ ds }}'
      -- 排除 momo 的福利品與整新品
      AND momo.Name NOT LIKE '%福利品%'
      AND momo.Name NOT LIKE '%整新品%'
      AND momo.Name NOT LIKE '%展示機%'

    UNION ALL

    SELECT 
        pch.scraped_date, dim.brand, dim.official_model_name, 'pchome' AS platform, pch.ID AS original_code, pch.Price AS price,
        ROW_NUMBER() OVER(PARTITION BY pch.ID, pch.scraped_date ORDER BY LENGTH(dim.keyword) DESC) AS rank_id
    FROM stg_pchome_prices pch
    JOIN dim_products dim ON LOWER(pch.Name) LIKE CONCAT('%', dim.keyword, '%')
    WHERE pch.scraped_date = '{{ ds }}'
      -- 排除 PChome 的福利品與整新品
      AND pch.Name NOT LIKE '%福利品%'
      AND pch.Name NOT LIKE '%整新品%'
      AND pch.Name NOT LIKE '%拆封%'
) combined_platforms
WHERE rank_id = 1;
