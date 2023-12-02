#!/bin/bash

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsu load_users_from_csv
gunicorn folha_ponto.wsgi:application --bind 0.0.0.0:10000
