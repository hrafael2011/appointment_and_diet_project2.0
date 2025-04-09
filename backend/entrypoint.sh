#!/bin/bash
set -e

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn DraFitApi.wsgi:application --bind 0.0.0.0:8000 --workers 4