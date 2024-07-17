from django.db import models


class FrequentRequest(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество запросов')

    class Meta:
        ordering = ['count']


class UserRequest(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Время запроса')
    user = models.ForeignKey('users.User', related_name='requests', on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        ordering = ['-request_date']
