from django.shortcuts import render

from forecast.models import FrequentRequest, UserRequest
from forecast.utils.get_json import DataGetter


def index(request):
    city = request.GET.get('city')
    days = request.GET.get('days')

    context = {
        'title': 'Главная',
        'freq_requests': FrequentRequest.objects.all().order_by('-count')[:5],
        'has_info': False
    }

    if not request.user.is_anonymous:
        context['user_requests'] = UserRequest.objects.filter(user=request.user).order_by('-request_date')[:3]

    if city:
        data, city_name = DataGetter.get_forecast(city, days)

        context['data'] = data
        context['city'] = city_name
        context['has_info'] = True

        # увеличение счетчика запросов
        if FrequentRequest.objects.filter(city=city_name).exists():
            freq_req = FrequentRequest.objects.get(city=city_name)
            freq_req.count += 1
            freq_req.save()
        else:
            FrequentRequest.objects.create(city=city_name)

        # трекер пользовательских запросов
        if not request.user.is_anonymous:
            UserRequest.objects.create(city=city_name, user=request.user)

    return render(request, 'forecast/index.html', context)
