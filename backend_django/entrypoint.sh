#!/bin/sh
echo "running the migration:"

python manage.py migrate --noinput || echo "Migration skipped"

echo "Starting Gunicorn on port $PORT..."
gunicorn backend.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 2 \
  --timeout 120