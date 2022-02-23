from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

app = Celery('django_celery', broker='amqp://guest:guest@localhost:5672//')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello_every_seconds': {
            'task': 'App.tasks.CheckSite',
            'schedule': timedelta(seconds=30),
            'args': ()
        },
    }
)
