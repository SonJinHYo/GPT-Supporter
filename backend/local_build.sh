#!/bin/sh

# [local] 
python3 manage.py makemigrations --settings=config.settings.local
python3 manage.py migrate --settings=config.settings.local 

# Django Superuser 생성
python3 manage.py shell --settings=config.settings.local <<EOF
from users.models import User
 
# 이미 존재하는 사용자 확인
user=User.objects.filter(username='$USERNAME')

# 새로운 관리자 계정 생성
if not user.exists():
    User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')
    print("관리자 계정 생성")

EOF

python3 manage.py runserver 0.0.0.0:8000 --settings=config.settings.local 
# gunicorn -c gunicorn_conf.py config.wsgi.local:application