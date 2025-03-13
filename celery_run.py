from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/0')

app.conf.beat_schedule = {
    'run_every_10_minutes': {
        'task': 'tasks.run_main',
        'schedule': 600.0  # 10 минут
    },
}


@app.task
def run_main():
    import asyncio

    from main import main
    asyncio.run(main())
