FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Добавляем путь к приложению в PYTHONPATH
ENV PYTHONPATH=/app

# Копируем только requirements.txt сначала
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Потом копируем остальные файлы
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
