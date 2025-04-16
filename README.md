# finance_bot

Bot responsible for managing and organizing personal finances.

## Setup

Make sure you have [Python]() and [uv]() installed on your machine.

```sh
uv venv
uv sync
```

### Running the API

```sh
docker compose up postgres

python manage.py migrate
python manage.py runserver
```

### Chat mode

```sh
python manage.py migrate
python manage.py chat
```

## Deploy

Change `API_KEY` in `finance_bot.settings` and database password in `docker-compose.yml`.
