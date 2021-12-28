from django.contrib import admin

# Register your models here.
from weather_app.models import Subscription, WeatherForecast

admin.site.register(Subscription)
admin.site.register(WeatherForecast)