#!/bin/bash

# python manage.py collectstatic --no-input
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createdepartamento # Departamento-2024-04-20.csv
# python manage.py createuser # normal user
# python manage.py createsu # super user
# python manage.py load_tipo_receita # TipoReceita-2024-04-20.csv
# python manage.py load_feriado # Feriado-2024-04-20.csv
# python manage.py load_clientes # Cliente-2024-04-20.csv
# python manage.py createprofile # UserProfile
# python manage.py load_pontos_pandas # Ponto-2024-04-20.csv
# gunicorn folha_ponto.wsgi:application --bind 0.0.0.0:10000
[“python”, “manage.py”, “runserver”, ‘0.0.0.0:10000’]
