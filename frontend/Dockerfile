FROM nginx:stable-alpine

# custom 설정파일을 컨테이너 내부로 복사한다.
COPY ./nginx.conf /etc/nginx/nginx.conf

# build 파일 복사
COPY ./build /usr/share/nginx/html

# 컨테이너의 80번 포트를 열어준다.
EXPOSE 80

# nginx 서버를 실행하고 백그라운드로 동작하도록 한다.
CMD ["nginx", "-g", "daemon off;"]