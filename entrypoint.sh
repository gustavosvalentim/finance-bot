#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Run Django server
daphne finance_bot.asgi:application --bind 0.0.0.0:8000 --workers 1 --daemon

# Run Telegram Bot
python manage.py telegram_bot