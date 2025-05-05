#!/bin/bash

# Проверяем наличие .env
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

# Останавливаем старые контейнеры
docker compose down

# Собираем и запускаем
docker compose up --build -d

echo "Waiting for database..."
sleep 5

# Показываем статус
docker compose ps

echo "==================================="
echo "Project is running!"
echo "API: http://localhost:8000"
echo "Swagger: http://localhost:8000/api/docs"
echo "ReDoc: http://localhost:8000/api/redoc"
echo "==================================="

# Показываем логи бэкенда
docker compose logs -f backend
