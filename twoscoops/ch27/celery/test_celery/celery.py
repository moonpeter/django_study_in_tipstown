from __future__ import absolute_import
from celery import Celery

app = Celery('test_celery',
            broker='amqp://doky:doky123@localhost/doky_host',
            backend='rpc://',
            include=['test_celery.tasks'])
