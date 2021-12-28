import weather.settings as settings
from weather_app.core import get_email_list, get_email_message, get_weather_object, aggregate_weather_data
from django.core.mail import send_mail
import datetime
from datetime import timedelta
from celery import shared_task


@shared_task
def send_emails(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD):
    email_list = get_email_list()
    message = get_email_message()
    for curr_email in email_list:
        send_mail(
            subject='The weather forecast for {date}'.format(
                date=(datetime.datetime.utcnow() + timedelta(hours=2)).date()
            ),
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[curr_email],
            auth_user=user,
            auth_password=password
        )
        print(f"Email sent to {curr_email}")


@shared_task
def update_weather_data(api_key=settings.WEATHER_API_KEY):
    weather_object = get_weather_object()
    weather_object.forecast = aggregate_weather_data(api_key=api_key)
    weather_object.save()
