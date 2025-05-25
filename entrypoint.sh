#!/bin/sh

python manage.py migrate

# Run Telegram Bot
python manage.py telegram_bot

# Run Django server
gunicorn finance_bot.wsgi:application --bind 0.0.0.0:8000 --workers 4