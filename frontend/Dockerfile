FROM node:19.6.1-alpine3.17 as builder

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

RUN rm .env

FROM nginx:stable-alpine


# build 파일 복사
COPY --from=builder /app/build /usr/share/nginx/html

# custom 설정파일을 컨테이너 내부로 복사한다.
COPY ./nginx.conf /etc/nginx/nginx.conf

# 컨테이너의 80번 포트를 열어준다.
EXPOSE 80

# nginx 서버를 실행하고 백그라운드로 동작하도록 한다.
CMD ["nginx", "-g", "daemon off;"]