#!/bin/sh

# [local] 
python3 manage.py makemigrations --settings=config.settings.local
python3 manage.py migrate --settings=config.settings.local 
python3 manage.py runserver 0.0.0.0:8000 --settings=config.settings.local 
# gunicorn -c gunicorn_conf.py config.wsgi.local:application