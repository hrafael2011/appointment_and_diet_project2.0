#!/bin/bash


#set -e

#echo "Aplicando migraciones..."
#python manage.py makemigrations --noinput
#python manage.py migrate --noinput

#echo "Recopilando archivos estáticos..."
#python manage.py collectstatic --noinput

#echo "Iniciando Gunicorn..."
#exec gunicorn DraFitApi.wsgi:application --bind 0.0.0.0:8000 --workers 4




#!/bin/bash
set -e

if [ "$APP_ROLE" = "backend" ]; then
  echo "Aplicando migraciones..."
  python manage.py makemigrations --noinput
  python manage.py migrate --noinput

  echo "Recopilando archivos estáticos..."
  python manage.py collectstatic --noinput
fi

# Lógica para elegir qué servicio iniciar
case "$APP_ROLE" in
  backend)
    echo "Iniciando Gunicorn..."
    exec gunicorn DraFitApi.wsgi:application --bind 0.0.0.0:8000 --workers 4
    ;;
  celery)
    echo "Iniciando Celery Worker..."
    exec celery -A DraFitApi.celery:app worker --loglevel=info
    ;;
  flower)
    echo "Iniciando Flower..."
    exec celery -A DraFitApi.celery:app flower --port=5555
    ;;
  *)
    echo "Error: APP_ROLE no definido correctamente"
    exit 1
    ;;
esac
