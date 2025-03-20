FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-distutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --with dev --no-root

COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic

RUN rm -rf alembic/versions && mkdir -p alembic/versions

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 80 --reload"]
