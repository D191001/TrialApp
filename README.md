# TrialApp

Бэкенд-сервис с авторизацией через Яндекс OAuth2 и системой комментариев.

## Функциональность

- Авторизация пользователей через Яндекс OAuth2
- Управление профилями пользователей
- Система поиска и матчинга пользователей
- Чат-комнаты с WebSocket поддержкой
- Система лайков и матчей
- Система комментариев для авторизованных пользователей
- REST API endpoints для работы с данными

## Технологии

- Python FastAPI
- PostgreSQL
- WebSocket для real-time чата
- PostgreSQL (LISTEN/NOTIFY) чат
- Docker
- GitHub Actions CI/CD
- Аутентификация через Яндекс OAuth2
- JWT токены

## API Endpoints

### Авторизация
- `POST /auth/yandex` - получение URL для авторизации
- `GET /auth/yandex/callback` - обработка callback от Яндекса

### Пример сценария

Клиент инициирует вход через Яндекс.

Получает OAuth-токен.

Отправляет этот токен на ваш backend.

Backend валидирует токен через Яндекс, получает профиль пользователя.

Создаёт/ищет пользователя в вашей базе.

Генерирует свой JWT-токен и отдаёт его клиенту.

Клиент использует ваш JWT-токен для дальнейшей работы с вашим API.



### Профиль
- `GET /profile` - получение профиля
- `PUT /profile` - обновление профиля
- `POST /profile/photos` - загрузка фото

### Поиск и матчинг
- `GET /search` - поиск пользователей
- `POST /likes/{user_id}` - добавить лайк
- `DELETE /likes/{user_id}` - удалить лайк
- `GET /matches` - получить матчи

### Комнаты и сообщения
- `POST /rooms` - создание комнаты
- `GET /rooms/{room_id}` - информация о комнате
- `POST /rooms/{room_id}/invite` - приглашение в комнату
- `POST /rooms/{room_id}/messages` - отправка сообщения
- `GET /rooms/{room_id}/messages` - история сообщений

### WebSocket
- `WebSocket /ws/{room_id}` - real-time чат в комнате

## API Документация

Документация API доступна по следующим адресам:
- Swagger UI: https://trialapp.ru/api/docs
- ReDoc: https://trialapp.ru/api/redoc

## Комментарии

- Авторизация через Яндекс OAuth2 обязательна
- Поддерживается древовидная структура (ответы на комментарии)
- Пагинация (limit/offset)
- Soft delete для комментариев
- Безопасность: SQLAlchemy ORM, JWT-токены

## Развертывание

Проект использует Docker и docker-compose для развертывания:

```bash
docker compose up -d
```

## Переменные окружения

Основные переменные окружения:
- `POSTGRES_*` - настройки базы данных
- `YANDEX_CLIENT_*` - настройки OAuth Яндекс
- `JWT_SECRET` - секретный ключ для JWT токенов

## Доступ

Проект доступен по адресу: https://trialapp.ru

## Тестирование

### Установка зависимостей для тестов
```bash
pip install -r requirements-test.txt
```

### Настройка тестовой базы данных
```bash
export TEST_DATABASE_URL="postgresql://test:test@localhost:5432/test_db"
```

### Запуск тестов
```bash
# Запуск всех тестов
pytest -v

# Запуск конкретной группы тестов
pytest tests/test_auth.py -v
pytest tests/test_profile.py -v

# Запуск тестов с покрытием кода
pytest --cov=app tests/
```

### Группы тестов
- `test_auth.py` - тесты аутентификации
- `test_profile.py` - тесты профиля пользователя
- `test_search.py` - тесты поиска
- `test_likes.py` - тесты лайков и матчей
- `test_rooms.py` - тесты комнат
- `test_messages.py` - тесты сообщений
- `test_websocket.py` - тесты WebSocket


