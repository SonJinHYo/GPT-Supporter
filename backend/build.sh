#!/bin/sh

# [local]
# python3 manage.py makemigrations --settings=config.settings.local
# python3 manage.py migrate --settings=config.settings.local
# gunicorn -c gunicorn_conf.py config.wsgi:application

# product
python3 manage.py makemigrations --settings=config.settings.prod
python3 manage.py migrate --settings=config.settings.prod
gunicorn -c gunicorn_conf.py config.wsgi:application