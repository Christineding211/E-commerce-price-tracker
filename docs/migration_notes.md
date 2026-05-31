# Migration Notes

## Distributed crawler scripts removed

The previous distributed crawler Python scripts were removed after migrating the workflow to Airflow.

Reason:
- Airflow DAGs now manage scheduling and orchestration.
- Celery workers are launched through Airflow worker services.
- The old scripts are no longer part of the production workflow.

Removed files:
- producer_crawler.py
- producer_multi_queue_test.py
- producer_multi_queue.py

