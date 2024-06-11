# get initial time
start=`date +%s`
echo "Running seed script..."
python manage.py makemigrations
python manage.py migrate
python manage.py flush
python manage.py createsu # 0. eduardo as superuser
python manage.py createdepartamento # 1. Departamento-current.csv
python manage.py load_tipo_receita # 2. TipoReceita-current.csv
python manage.py createuser # 3. normal user
python manage.py createprofile # 4. UserProfile-current.csv
python manage.py load_feriado # 5. Feriado-current.csv
python manage.py load_ferias # 6. Ferias-current.csv
# python manage.py load_refeicao # 7. Refeicao-current.csv
python manage.py load_clientes # 8. Cliente-current.csv
python manage.py load_pontos # 9. Ponto-current.csv
# get final time
end=`date +%s`
# calculate execution time
runtime=$((end-start))
# translate seconds to minutes
minutes=$((runtime/60))
echo "Execution time: $minutes minutes"
