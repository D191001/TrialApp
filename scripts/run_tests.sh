#!/bin/bash

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements-test.txt

# Настройка переменных окружения
export TESTING=1
export PYTHONPATH="${PWD}/backend"

# Запуск тестов
cd backend
python -m pytest tests/ -v -s
