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

echo "loading states fixture..." 
python3 manage.py loaddata cars/fixtures/states.json || echo "fixture já carregada ou não encontrada"

echo "collecting static files"
python3 manage.py collectstatic --noinput

echo "starting gunicorn..."
exec "$@"
