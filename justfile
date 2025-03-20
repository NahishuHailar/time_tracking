up:
    docker-compose up -d

test:
    pytest tests/

lint:
    poetry run ruff check --fix .
    poetry run ruff format .
    poetry run black .

migrate:
    alembic upgrade head