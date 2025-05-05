#!/bin/bash

# Проверяем есть ли права sudo
if [ "$(id -u)" != "0" ]; then
   echo "Этот скрипт должен быть запущен с правами root" 
   exec sudo "$0" "$@"
   exit
fi

# Останавливаем PostgreSQL
systemctl stop postgresql

# Настраиваем конфигурацию PostgreSQL
pg_version=$(ls /etc/postgresql/)
pg_hba="/etc/postgresql/$pg_version/main/pg_hba.conf"

# Обновляем метод аутентификации
sed -i 's/peer/trust/g' $pg_hba
sed -i 's/md5/trust/g' $pg_hba

# Запускаем PostgreSQL
systemctl start postgresql

# Создаем тестовую БД и пользователя
su - postgres -c "psql -c \"CREATE USER trump WITH SUPERUSER PASSWORD 'password';\" || true"
su - postgres -c "psql -c \"CREATE DATABASE test_db OWNER trump;\" || true"

echo "PostgreSQL настроен успешно!"
