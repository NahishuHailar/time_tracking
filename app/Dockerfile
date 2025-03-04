FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей (ускоряет сборку за счёт кэша)
COPY ../pyproject.toml ../poetry.lock ./
# Устанавливаем зависимости
RUN poetry install --no-root --with dev

# Теперь копируем весь код проекта
COPY ../ ./

# Запуск FastAPI-приложения (указываем PYTHONPATH перед запуском)
CMD ["sh", "-c", "PYTHONPATH=/app poetry run uvicorn app.main:app --host 0.0.0.0 --port 80 --reload"]
