

from airflow.operators.python import PythonOperator

# 匯入外部的 Producer 邏輯
from crawler.producer_multi_queue import dispatch_tasks

def run_producer_dispatch():
    
    print("Airflow is launching the external crawler dispatcher (Producer)")
    dispatch_tasks()
    print("Tasks successfully dispatched to RabbitMQ.")

def create_trigger_producer_task() -> PythonOperator:
    return PythonOperator(
        task_id="trigger_crawler_producer",
        python_callable=run_producer_dispatch,
    )
