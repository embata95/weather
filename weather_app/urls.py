from django.urls import path, include
from rest_framework import routers
from weather_app.views import Subscribe, home_view, weather_API, SubscribeAPI

router = routers.DefaultRouter()
router.register(r'subscribe-API', SubscribeAPI)

urlpatterns = [
    path('', home_view, name='home_view'),
    path('<int:pk>', home_view, name='home_view'),
    path('subscribe/', Subscribe.as_view(), name='subscribe_view'),
    path('weather-info/', weather_API, name='web API'),
    path('', include(router.urls))
]