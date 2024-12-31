from __future__ import absolute_import

from django_celery.celery import app

@app.task
def say_hello():
    print("Hello World")
