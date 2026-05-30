

#from crawler.worker import app --> only use in celery 

from airflow.operators.python import PythonOperator
from crawler.tasks_crawler import crawler_pchome_print, scrape_momo


TARGET_CONFIGS = [
    {"brand": "Sony", "q": "Sony WH"},
    {"brand": "Sennheiser", "q": "Sennheiser 降噪耳機"},
    {"brand": "JLAB", "q": "JLAB 降噪耳機"},
    {"brand": "Soundcore", "q": "Soundcore 降噪耳機"},
]


def create_scraper_tasks():
    """
    Create Airflow PythonOperator tasks for PChome and momo scraping.

    In Method A, Airflow CeleryExecutor distributes these PythonOperator tasks
    to Airflow workers. We do NOT use crawler Celery .delay() or .apply_async().
    """

    pchome_tasks = []
    momo_tasks = []

    for config in TARGET_CONFIGS:
        brand = config["brand"]
        keyword = config["q"]

        safe_brand = brand.lower().replace(" ", "_")

        pchome_task = PythonOperator(
            task_id=f"scrape_pchome_{safe_brand}",
            python_callable=crawler_pchome_print,
            op_kwargs={
                "brand_name": brand,
                "search_keyword": keyword,
            }
            
        )

        momo_task = PythonOperator(
            task_id=f"scrape_momo_{safe_brand}",
            python_callable=scrape_momo,
            op_kwargs={
                "brand_name": brand,
                "keywords": keyword,
            }
            
        )

        pchome_tasks.append(pchome_task)
        momo_tasks.append(momo_task)

    return pchome_tasks, momo_tasks
