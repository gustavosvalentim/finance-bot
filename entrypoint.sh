#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Run Django server
nohup daphne finance_bot.asgi:application --bind 0.0.0.0:8000 &

# Run Telegram Bot
python manage.py telegram_bot