from django.shortcuts import render
import requests
from datetime import datetime
from django.http import HttpResponse, JsonResponse

from weather_api import current_weather
from django.http import JsonResponse


# def my_view(request):
#     if request.method == "GET":
#         data = current_weather(59.93, 30.31)  # Результат работы функции current_weather
#         # А возвращаем объект JSON. Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
#         # как помните это необходимо для корректного отображения кириллицы
#         return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                      'indent': 4})


def weather_view(request):  # более гибкая функция
    if request.method == "GET":  # при обработке запроса https://example.ru?q=запрос&a=ответ из request.GET
        # получим словарь {'q': 'запрос', 'a': 'ответ'}
        lat = request.GET.get('lat')  # данные придут в виде строки
        lon = request.GET.get('lon')  # данные придут в виде строки
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)  # если ничего не передать, то погода будет в Санкт-Петербурге
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
