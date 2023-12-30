docker-compose exec web-folha python manage.py collectstatic --no-input
docker-compose exec web-folha python manage.py makemigrations
docker-compose exec web-folha python manage.py migrate
docker-compose exec web-folha python manage.py createuser # normal user
docker-compose exec web-folha python manage.py createsu # super user
docker-compose exec web-folha python manage.py load_tipo_receita # Tipo Receita
docker-compose exec web-folha python manage.py load_contato # Contatos
docker-compose exec web-folha python manage.py load_feriado # Feriados
docker-compose exec web-folha python manage.py load_clientes # Clientes
docker-compose exec web-folha python manage.py load_pontos_pandas # Pontos-2023
