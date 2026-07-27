-- cleaning fct_daily_prices
with source_data as (

    select
        scraped_date,
        brand,
        official_model_name,
        platform,
        original_code,
        price
    from {{ source('ecommerce', 'fct_daily_prices') }}
),

cleaned_data as (

    select
        cast(scraped_date as date) as scraped_date,
        trim(brand) as brand,
        trim(official_model_name) as official_model_name,
        lower(trim(platform)) as platform,
        cast(original_code as string) as original_code,
        safe_cast(price as numeric) as price
    from source_data

)

select
    scraped_date,
    brand,
    official_model_name,
    platform,
    original_code,
    price
from cleaned_data
where scraped_date is not null
  and brand is not null
  and official_model_name is not null
  and platform in ('momo', 'pchome')
  and price is not null
  and price > 0

