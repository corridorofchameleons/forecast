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
        elif city_name != 'undefined':
            FrequentRequest.objects.create(city=city_name)

        # трекер пользовательских запросов
        if request.user.is_authenticated:
            if city_name != 'undefined':
                UserRequest.objects.create(city=city_name, user=request.user)

            # поскольку sqlite не поддерживает DISTINCT ON, делаем логику руками
            q = UserRequest.objects.filter(user=request.user).order_by('-request_date').values_list('city',
                                                                                                    flat=True)
            user_cities = set()
            for s in q:
                print(s, user_cities)
                if len(user_cities) < 5:
                    user_cities.add(s)
                else:
                    break
            context['user_cities'] = user_cities

    return render(request, 'forecast/index.html', context)
