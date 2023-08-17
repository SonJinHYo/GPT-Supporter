#!/bin/sh

# [local]
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000

# # product
# python3 manage.py makemigrations --settings=config.settings.prod
# python3 manage.py migrate --settings=config.settings.prod
# gunicorn -c gunicorn_conf.py config.wsgi:application