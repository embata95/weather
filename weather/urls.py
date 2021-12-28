from django.contrib import admin
from django.urls import path, include
from weather.tasks import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather_app.urls'))
]
