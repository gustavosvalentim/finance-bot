#!/bin/sh

python manage.py migrate

gunicorn finance_bot.wsgi:application --bind 0.0.0.0:8000 --workers 4