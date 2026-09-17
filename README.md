# Shop API

REST API для интернет-магазина на FastAPI. Позволяет управлять каталогом товаров, пользователями и заказами.

## Стек

- **FastAPI** — веб-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy (async) + asyncpg** — ORM и драйвер
- **Pydantic v2** — валидация и сериализация
- **Poetry** — управление зависимостями
- **Docker Compose** — запуск инфраструктуры

## Архитектура

```
HTTP-запрос
    ↓
routers/        — эндпоинты FastAPI
    ↓
services/       — бизнес-логика (в разработке)
    ↓
repositories/   — CRUD к БД (в разработке)
    ↓
models/         — SQLAlchemy-модели
    ↓
PostgreSQL
```

- **`routers/`** — принимают HTTP-запросы, валидируют через Pydantic, вызывают сервисы.
- **`models/`** — SQLAlchemy-модели таблиц.
- **`schemas/`** — Pydantic-схемы: что приходит и что уходит через API.
- **`db/`** — подключение к PostgreSQL, создание async-сессии.
- **`main.py`** — точка входа: создаёт приложение, подключает роутеры, настраивает lifespan.

## Запуск

### Через Poetry

1. Установите зависимости:

   ```bash
   poetry install
   ```

2. Поднимите PostgreSQL в Docker:

   ```bash
   docker compose up -d
   ```

3. Запустите приложение:

   ```bash
   poetry run uvicorn main:app --reload
   ```

Swagger будет доступен на `http://127.0.0.1:8000/docs`.

### Переменные окружения

Настройки подключения к БД лежат в `db/postgres.py`. По умолчанию:

```
postgresql+asyncpg://user:password@localhost:5433/shop
```

Порт `5433` — внешний порт контейнера (внутри PostgreSQL слушает `5432`).

## Эндпоинты

| Метод | Путь | Что делает |
|---|---|---|
| POST | `/products` | Создаёт товар |
| GET | `/products` | Список товаров с пагинацией (`limit`, `offset`) |
| GET | `/products/{product_id}` | Один товар по ID |
| POST | `/users` | Создаёт пользователя |
| GET | `/users/{user_id}` | Один пользователь по ID |
| POST | `/orders` | Создаёт заказ, возвращает `order_id` и `total` |
| GET | `/stats/top-products` | Топ-5 товаров по количеству продаж |

## Архитектурные решения

### PostgreSQL для всех сущностей

Изначально проект использовал polyglot persistence: MySQL для пользователей и заказов, MongoDB для товаров. В процессе рефакторинга я перенёс всё в PostgreSQL, потому что:

- Товары имеют предсказуемую структуру (`name`, `description`, `price`), которая хорошо ложится в реляционную модель.
- Транзакции при создании заказа проще, когда все данные в одной БД.
- Меньше инфраструктуры — проще деплой и тесты.

MongoDB была бы оправдана, если бы у товаров были сильно разные наборы полей (например, техника vs одежда). В текущей модели это не так.

### Асинхронный SQLAlchemy

Проект использует `asyncpg` и `AsyncSession` — FastAPI работает в async-режиме, и блокирующие запросы к БД свели бы на нет преимущества async. Все операции с БД — через `await`.

### Пагинация

В `GET /products` параметр `offset` — это **номер страницы** (0, 1, 2, ...). Внутри используется `skip(offset * limit).limit(limit)`.

## Что было сложного

1. **Перенос хранилища.** Изначально товары хранились в MongoDB. Переход на PostgreSQL потребовал переписать модели, схемы, роутеры и запросы. Самое сложное — согласовать типы: `ObjectId` → `int`, `str` → `UUID`, а также убрать остатки Mongo (`alias='_id'`, `bson.ObjectId`) из схем.

2. **Смешение sync и async.** SQLAlchemy имеет sync и async API. Сначала роутеры были sync (`def`, `Session`), а движок — async (`AsyncSession`). Это давало странные ошибки (`id=None` после `commit`, `coroutine was never awaited`). Пришлось привести всё к async.

3. **`relationship` без `ForeignKey`.** SQLAlchemy не может построить связь между таблицами, если нет внешнего ключа. Ошибка `NoForeignKeysError` вылезла при первом `POST /products`, потому что SQLAlchemy лениво строит маппинги.

## Планы

- [ ] UUID вместо int для ID
- [ ] Слой репозиториев и сервисов
- [ ] JWT-авторизация
- [ ] Тесты (pytest)
- [ ] Alembic-миграции
- [ ] CI на GitHub Actions

## Автор

[xenoval](https://github.com/xenoval)
