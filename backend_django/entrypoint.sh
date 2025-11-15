#!/bin/sh
echo "running the migration:"

python manage.py migrate

echo "starting the server:"
python manage.py runserver 0.0.0.0:8000