#!/bin/sh

python manage.py migrate

python manage.py collectstatic --noinput

# Run Django server
gunicorn finance_bot.wsgi:application --bind 0.0.0.0:8000 --workers 1 -d

# Run Telegram Bot
python manage.py telegram_bot