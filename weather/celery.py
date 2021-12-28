import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

app = Celery('weather')

app.conf.beat_schedule = {
    'send mails': {
        'task': 'weather.tasks.send_emails',
        'schedule': crontab(hour=5, minute=0),
    },
    'get weather data': {
        'task': 'weather.tasks.update_weather_data',
        'schedule': crontab(hour=4, minute=0),
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
if __name__ == '__main__':
    app.start()
