#!/bin/bash

# Проверка и запуск PostgreSQL
if ! pg_isready; then
    echo "Starting PostgreSQL..."
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
    sleep 5  # Ждем запуска
fi

# Настройка доступа к PostgreSQL
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo -u postgres psql -c "CREATE DATABASE test_db;" || true

# Настройка pg_hba.conf для доступа по паролю
PG_HBA_FILE=$(sudo -u postgres psql -t -P format=unaligned -c 'SHOW hba_file;')
sudo sed -i '/^host.*all.*all.*127.0.0.1\/32.*ident/c\host    all             all             127.0.0.1/32            md5' $PG_HBA_FILE

# Перезапуск PostgreSQL для применения изменений
sudo systemctl restart postgresql
sleep 3  # Ждем перезапуска

# Создание виртуального окружения если его нет
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r backend/requirements.txt
pip install -r requirements-test.txt
pip install pydantic-settings

# Создание пользователя PostgreSQL с правами
sudo -u postgres psql -c "CREATE USER trump WITH PASSWORD 'password' SUPERUSER CREATEDB;" || true

# Пересоздание тестовой базы данных
dropdb -U trump test_db --if-exists
createdb -U trump test_db

# Настройка переменных окружения
export DATABASE_URL="postgresql://trump:password@localhost:5432/test_db"
export PYTHONPATH="${PWD}/backend:${PYTHONPATH}"

echo "Test environment setup completed!"
