# finance_bot

Change `API_KEY` in `finance_bot.settings` and database password in `docker-compose.yml`.

## Setup

Make sure you have [Python]() and [uv]() installed on your machine.

```sh
uv sync
uv venv
```

### Running the API

```sh
python manage.py migrate
python manage.py runserver
```

### Chat mode

```sh
python manage.py run_agents
```
