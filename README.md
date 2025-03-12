# ParseIndicator


docker network create mynetwork

# Запуск MongoDB
docker run -d --name mongo --network mynetwork -p 27017:27017 mongo

# Сборка контейнера со скриптом
docker build -t my_script .

# Запуск контейнера
docker run --rm --network mynetwork my_script
