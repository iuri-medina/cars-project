#!/bin/bash

echo "waiting for postgres..."
until nc.traditional -z db 5432; do
  echo "Postgres ainda não está pronto. Aguardando..."
  sleep 1
done


echo "postgres is up, running migrations..."
python3 manage.py migrate --noinput

echo "collecting static files"
python3 manage.py collectstatic --noinput

echo "starting gunicorn..."
exec "$@"
