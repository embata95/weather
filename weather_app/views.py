from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from weather_app.core import filter_weather_data
from weather_app.models import Subscription, WeatherForecast
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class Subscribe(CreateView):
    model = Subscription
    fields = '__all__'
    template_name = 'subscribe.html'
    success_url = reverse_lazy('home_view')


def home_view(request, pk=7):
    context = {
        'data': filter_weather_data(pk=pk),
    }
    return render(request, 'index.html', context=context)


@api_view(['GET'])
def weather_API(request):
    days = 7
    if 'days' in request.query_params:
        days = int(request.query_params['days'])
    return Response(data=filter_weather_data(pk=days))


class SubscribeAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscribeAPI(viewsets.ModelViewSet):
    http_method_names = 'post'
    queryset = Subscription.objects.all()
    serializer_class = SubscribeAPISerializer
