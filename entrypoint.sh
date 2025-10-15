#!/bin/bash

echo "waiting for postgres..."
until nc.traditional -z db 5432; do
  echo "Postgres ainda não está pronto. Aguardando..."
  sleep 1
done


echo "postgres is up, making migrations..."
python3 manage.py makemigrations

echo "running migrations..."
python3 manage.py migrate --noinput

echo "loading fixtures: states and brands..." 
python3 manage.py loaddata cars/fixtures/states.json cars/fixtures/brands.json || echo "fixtures já carregadas ou não encontradas"

echo "collecting static files"
python3 manage.py collectstatic --noinput

echo "starting gunicorn..."
exec "$@"
