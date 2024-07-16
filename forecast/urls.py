from django.urls import path

from forecast.apps import ForecastConfig
from forecast.views import index

app_name = ForecastConfig.name

urlpatterns = [
    path('', index, name='index')
]