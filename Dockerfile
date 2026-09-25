FROM python:3.12-slim

# Python не буферизует stdout — логи сразу видны в docker logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Системные зависимости для psycopg2 и сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==2.4.3 \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# Сначала только зависимости — для кэша слоёв
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

# Потом код
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]