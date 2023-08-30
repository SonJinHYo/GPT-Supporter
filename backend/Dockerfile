FROM python:3.9-alpine

RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "--upgrade", "setuptools","wheel"]
RUN ["apk", "update"]
RUN ["apk", "add", "--no-cache", "gcc","musl-dev", "libffi-dev","openssl-dev","mariadb-dev"]

WORKDIR /app

COPY requirements.txt .

RUN ["pip","install","-r","requirements.txt"]

COPY . .

ARG DEFAULT_PORT=8000

EXPOSE ${DEFAULT_PORT}


COPY prod_build.sh /prod_build.sh
RUN chmod +x /prod_build.sh

ENTRYPOINT ["/prod_build.sh"]