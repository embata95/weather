from django.db import models


class Subscription(models.Model):
    email = models.EmailField(unique=True)


class WeatherForecast(models.Model):
    forecast = models.JSONField(default=dict)
