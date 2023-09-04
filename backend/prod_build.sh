#!/bin/sh

# product
python3 manage.py makemigrations --settings=config.settings.prod
python3 manage.py migrate --settings=config.settings.prod

python3 manage.py shell --settings=config.settings.local <<EOF
from users.models import User
 
# 이미 존재하는 사용자 확인
user=User.objects.filter(username='$USERNAME')

# 새로운 관리자 계정 생성
if not user.exists():
    User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')
    print("관리자 계정 생성")

EOF

gunicorn -c gunicorn_conf.py config.wsgi.prod:application