from django.shortcuts import render

from forecast.utils.get_json import DataGetter


def index(request):
    city = request.GET.get('city')
    days = request.GET.get('days')

    data, city_name = DataGetter.get_forecast(city, days)

    context = {
        'data': data,
        'city': city_name,
    }

    return render(request, 'forecast/index.html', context)
