import logging
import os
import nest_asyncio
from celery import Celery

logging.basicConfig(level=logging.INFO)
app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'))
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    'run_every_10_minutes': {
        'task': 'tasks.run_main',
        'schedule': 900.0  # 15 минут
    },
}

nest_asyncio.apply()

@app.task
def run_main():
    import asyncio
    from main import main

    logging.info("Starting run_main task")
    try:
        asyncio.run(main())
        logging.info("run_main task completed successfully")
    except Exception as e:
        logging.error(f"run_main task failed: {e}")