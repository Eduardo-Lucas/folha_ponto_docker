#!/bin/bash

# python manage.py collectstatic --no-input
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createdepartamento # Departamento-2024-05-10.csv
# python manage.py createuser # normal user
# python manage.py createsu # super user
# python manage.py load_tipo_receita # TipoReceita-2024-05-10.csv
# python manage.py load_feriado # Feriado-2024-05-10.csv
# python manage.py load_clientes # Cliente-2024-05-10.csv
# python manage.py createprofile # UserProfile-2024-05-10.csv
# python manage.py load_pontos_pandas # Ponto-2024-04-20.csv
# gunicorn folha_ponto.wsgi:application --bind 0.0.0.0:10000

# brought build.sh commands here
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
# pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
