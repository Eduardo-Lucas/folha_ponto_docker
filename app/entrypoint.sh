#!/bin/bash

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py createdepartamento # Departamento
python manage.py createuser # normal user
python manage.py createsu # super user
python manage.py load_tipo_receita # Tipo Receita
# python manage.py load_contato # Contatos not needed anymore
python manage.py load_feriado # Feriados
python manage.py load_clientes # Clientes
# python manage.py createprofile # Profile
# python manage.py load_pontos_pandas # Pontos-2023
gunicorn folha_ponto.wsgi:application --bind 0.0.0.0:10000
