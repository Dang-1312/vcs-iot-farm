import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VCS_Farm.settings")
app = Celery("Sub_thread")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()