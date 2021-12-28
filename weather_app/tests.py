import requests
from django.test import TestCase, Client
from weather.tasks import update_weather_data
from weather_app.core import get_email_list, get_email_message, filter_weather_data, get_weather_object, \
    get_weather_forecast, aggregate_weather_data
from weather_app.models import Subscription, WeatherForecast


class EmailTest(TestCase):
    def test_empty_email_list(self):
        self.assertListEqual(get_email_list(), [])

    def test_email_list_push(self):
        Subscription.objects.create(email="test@gmail.com")
        self.assertListEqual(get_email_list(), ["test@gmail.com"])

    def test_email_message_when_no_weather_object_exists(self):
        fail_msg = "Unfortunately the developer made a mistake and currently there is no data for today."
        self.assertEqual(get_email_message(), fail_msg)

    def test_email_message_when_weather_object_exists(self):
        success_msg = 'Today the min temperature will be {min_temp} and the max temperature will be {max_temp}!'
        update_weather_data()
        today_data = list(filter_weather_data(pk=1).values())[0]
        self.assertEqual(
            get_email_message(),
            success_msg.format(
                min_temp=today_data['min_temp'],
                max_temp=today_data['max_temp'],
            )
        )


class WeatherAPITest(TestCase):
    def test_get_weather_object_when_weather_object_is_not_created_yet(self):
        self.assertEqual(get_weather_object(), WeatherForecast.objects.first())

    def test_get_weather_object_when_weather_object_exists(self):
        WeatherForecast.objects.create(forecast={})
        self.assertEqual(get_weather_object(), WeatherForecast.objects.first())

    def test_get_weather_forecast_with_wrong_API_key(self):
        self.assertIsNone(get_weather_forecast(api_key='ThisIsNotAValidKey'))

    def test_aggregate_weather_data_with_wrong_API_key(self):
        self.assertEqual(aggregate_weather_data(api_key='ThisIsNotAValidKey'), {})

    def test_save_weather_forecast_data_with_wrong_API_key(self):
        update_weather_data(api_key='ThisIsNotAValidKey')
        self.assertEqual(WeatherForecast.objects.first().forecast, {})


class RESTAPITest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_get_weather_forecast(self):
        update_weather_data()
        response = self.client.get('http://127.0.0.1:8080/weather-info/?format=json')
        self.assertEqual(response.data, filter_weather_data(pk=7))

        response = self.client.get('http://127.0.0.1:8080/weather-info/?days=1&format=json')
        self.assertEqual(response.data, filter_weather_data(pk=1))

        response = self.client.get('http://127.0.0.1:8080/weather-info/?days=7&format=json')
        self.assertEqual(response.data, filter_weather_data(pk=7))

        response = self.client.get('http://127.0.0.1:8080/weather-info/?days=99&format=json')
        self.assertEqual(response.data, filter_weather_data(pk=7))

    def test_email_subscribe(self):
        response = self.client.post('http://127.0.0.1:8080/subscribe-API/', data={'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_email_list(), ['test@gmail.com'])

        response = self.client.post('http://127.0.0.1:8080/subscribe-API/', data={'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 400)
