import datetime

import requests
from weather import settings
from weather_app.models import Subscription, WeatherForecast
from datetime import timedelta


def filter_weather_data(pk=7):
    weather_data = {}
    if WeatherForecast.objects.exists():
        max_days = 7
        if pk > max_days:
            pk = max_days
        weather_object = WeatherForecast.objects.first()
        for x in dict(weather_object.forecast):
            temperatures = weather_object.forecast[x]['temps']
            if len(weather_data) < pk and temperatures:
                weather_data[x] = {
                    'day_name': weather_object.forecast[x]['day_name'],
                    'min_temp': min(temperatures),
                    'max_temp': max(temperatures)
                }
    return weather_data


def get_email_list():
    return list(Subscription.objects.all().values_list('email', flat=True))


def get_email_message():
    if WeatherForecast.objects.exists():
        today_data = list(filter_weather_data(pk=1).values())[0]
        message = 'Today the min temperature will be {min_temp} and the max temperature will be {max_temp}!'.format(
            min_temp=today_data['min_temp'],
            max_temp=today_data['max_temp']
        )
    else:
        message = "Unfortunately the developer made a mistake and currently there is no data for today."
    return message


def get_weather_object():
    if WeatherForecast.objects.exists():
        weather_object = WeatherForecast.objects.first()
    else:
        weather_object = WeatherForecast.objects.create(pk=1)
    return weather_object


def get_weather_forecast(api_key):
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 42.698334,
            'lng': 23.319941,
            'params': 'airTemperature',
            'start': (datetime.datetime.utcnow() + timedelta(hours=2)).date().isoformat()
        },
        headers={
            'Authorization': api_key
        }
    )
    if response.status_code != 200:
        return None
    json_data = response.json()
    return json_data


def aggregate_weather_data(api_key):
    weather_data = get_weather_forecast(api_key=api_key)
    my_dict = {}
    if weather_data:
        for curr_hour in weather_data['hours']:
            curr_date = curr_hour['time'].split('T')[0]
            if curr_date not in my_dict:
                my_dict[curr_date] = {
                    'temps': [curr_hour['airTemperature']['sg']],
                    'day_name': datetime.datetime.strptime(curr_date, '%Y-%m-%d').strftime("%A")
                }
            else:
                my_dict[curr_date]['temps'].append(curr_hour['airTemperature']['sg'])
    return my_dict

