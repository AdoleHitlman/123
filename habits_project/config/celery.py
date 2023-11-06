from celery import Celery

app = Celery('habits_project')

# Configure Celery app settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in the Django app
app.autodiscover_tasks()