#!/bin/bash
cd /data/web/project
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
sleep 3
echo "Apply database migrations"

python manage.py makemigrations 
python manage.py makemigrations app
python manage.py migrate
python manage.py migrate app

# Init Database (custom command from app for testing)
echo "Init Databaser"
python manage.py initapp

# Start server
echo "Starting server"
gunicorn -c /data/run/gunicorn.conf.py main.wsgi:application
