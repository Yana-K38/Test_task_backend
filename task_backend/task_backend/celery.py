from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_backend.settings')
app = Celery('task_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()