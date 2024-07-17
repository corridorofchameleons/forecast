from django.shortcuts import render

from forecast.utils.get_json import DataGetter


def index(request):
    city = request.GET.get('city')
    days = request.GET.get('days')

    context = {
        'title': 'Главная',
        'has_info': False
    }

    if city:
        data, city_name = DataGetter.get_forecast(city, days)

        context['data'] = data
        context['city'] = city_name
        context['has_info'] = True

    return render(request, 'forecast/index.html', context)
