FROM python:3.9.6-alpine3.13

RUN mkdir /app
WORKDIR /app

COPY ./* /app/

RUN apk --update add gcc musl-dev libgcc curl
RUN apk add mariadb-dev mariadb-client

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000
CMD /bin/sh