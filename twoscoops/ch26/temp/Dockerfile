FROM python:3.9.6-alpine3.13

RUN mkdir /app
WORKDIR /app

COPY ./* /app/

RUN pip install -r requirements.txt

EXPOSE 8000
CMD /bin/sh