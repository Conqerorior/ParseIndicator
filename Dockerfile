FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем скрипт запуска
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Указываем скрипт как точку входа
ENTRYPOINT ["/start.sh"]