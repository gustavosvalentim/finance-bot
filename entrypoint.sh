#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Run Telegram Bot
nohup python manage.py telegram_bot &

# Run Django server
daphne -b 0.0.0.0 -p 8000 finance_bot.asgi:application
