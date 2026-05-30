


-- if scraped failed, delete that day data to ensure no duplicated 
DELETE FROM stg_pchome_prices 
WHERE scraped_date = '{{ ds }}';

INSERT INTO stg_pchome_prices  (
    ID, 
    scraped_date, 
    Name, 
    Price, 
    Rating,  
    Source, 
    scraped_at
)
WITH deduplicated AS (
    SELECT 
        ID, 
        DATE(scraped_at) AS scraped_date, 
        Name, 
        Price, 
        Rating, 
        Source, 
        scraped_at,
        ROW_NUMBER() OVER(
            PARTITION BY ID, DATE(scraped_at) 
            ORDER BY scraped_at ASC
        ) AS row_num
    FROM raw_pchome_prices
    WHERE DATE(scraped_at) = '{{ ds }}' 
)

SELECT 
    ID, 
    scraped_date, 
    Name, 
    Price, 
    Rating, 
    Source, 
    scraped_at
FROM deduplicated
WHERE row_num = 1;

