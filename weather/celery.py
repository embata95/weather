import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')
# TODO: rabbitMQ or some kind of queue service needed and should be set as broker (refer to Celery's documentation for more info).
# TODO: add to documentation for Celery: Run the following command to start a worker that would execute the scheduled task "celery -A weather worker --loglevel=info --concurrency 1 -P solo"
# TODO: add to documentation for Celery: Run the following command to start the beat schedule process "celery -A weather beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
# TODO: describe the API

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
