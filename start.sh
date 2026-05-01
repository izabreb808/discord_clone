#!/usr/bin/env bash
set -o errexit

mkdir -p /var/data/media
python manage.py migrate
gunicorn discord_clone.wsgi:application --bind 0.0.0.0:${PORT:-8000}
