import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

data = requests.get('https://geocoding-api.open-meteo.com/v1/search?name=Moscow&count=1&language=en&format=json')

results = data.json().get('results')

if results:
    lat = results[0].get('latitude')
    lon = results[0].get('longitude')

    url = "https://api.open-meteo.com/v1/forecast?"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max",
        "forecast_days": 3
    }
    responses = openmeteo.weather_api(url, params=params)

    daily = responses[0].Daily()
    print(daily.Variables(0).Values(2))

