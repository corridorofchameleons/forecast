from datetime import timedelta

import requests
import openmeteo_requests
import requests_cache
from django.utils import timezone
from retry_requests import retry


class DataGetter:
    cache_session = requests_cache.CachedSession('.cache', expire_after=60)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast?"
    MAX_DAYS = 16

    @staticmethod
    def __get_coordinates(city):
        '''
        Получает координаты города.
        '''

        # во избежание кучи проверок предполагаем, что пользователь ищет большой город,
        # поэтому достаем только одно значение
        data = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json')

        result = data.json().get('results')[0]

        if result:
            lat = result.get('latitude')
            lon = result.get('longitude')
            name = result.get('name')

            return lat, lon, name
        return None

    @staticmethod
    def __get_temp(city, days, value):
        try:
            lat, lon, name = DataGetter.__get_coordinates(city)
        except TypeError:
            lat, lon, name = None, None, 'undefined'

        if lat and lon:
            params = {
                "latitude": lat,
                "longitude": lon,
                "forecast_days": days,
                "daily": f'temperature_2m_{value}'
            }
            responses = DataGetter.openmeteo.weather_api(DataGetter.url, params=params)
            return responses[0].Daily(), name
        return None

    @staticmethod
    def get_forecast(city, days):
        '''
        Получает прогноз погоды.
        (Упрощенный функционал)
        '''
        date = timezone.now()

        try:
            days = int(days)
        except:
            days = 3

        if days > DataGetter.MAX_DAYS:
            days = DataGetter.MAX_DAYS

        try:
            daily_min = DataGetter.__get_temp(city, days, 'min')[0]
            daily_max, name = DataGetter.__get_temp(city, days, 'max')
            result = []
            for i in range(days):
                result.append((date + timedelta(i, days), int(daily_min.Variables(0).Values(i)),
                               int(daily_max.Variables(0).Values(i))))
        except:
            result = [(date, 'undefined', 'undefined')]
            name = 'undefined'

        return result, name
