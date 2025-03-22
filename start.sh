#!/bin/bash

# Запуск Celery Worker
celery -A tasks worker --loglevel=info &

# Запуск Celery Beat
celery -A tasks beat --loglevel=info &

# Вызов задачи
celery -A tasks call tasks.run_main

# Бесконечный цикл, чтобы контейнер не завершался
while true; do
  sleep 1
done