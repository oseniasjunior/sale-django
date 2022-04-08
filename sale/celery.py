from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sale.settings')

app = Celery('sale')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('periodic', Exchange('periodic'), routing_key='periodic'),
)

TASKS = {
    'periodic_task': {
        'task': 'basic.tasks.periodic_task',
        'schedule': 5
    }
}

app.conf.beat_schedule = TASKS
app.autodiscover_tasks()
app.conf.timezone = 'America/Manaus'
