from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsaleproject.settings')

app = Celery('carsaleproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Configure periodic task to reset OTP attempts daily at 23:59:59
app.conf.beat_schedule = {
    'reset-otp-attempts': {
        'task': 'carsaleapp.custom_functions.reset_otp_attempts',
        'schedule': crontab(hour='23', minute='59', second='59'),
    },
}
