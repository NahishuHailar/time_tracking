up:
    docker-compose up -d

test:
    pytest tests/

lint:
    poetry run ruff check app tests

migrate:
    alembic upgrade head