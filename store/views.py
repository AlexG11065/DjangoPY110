from django.shortcuts import render

from django.http import JsonResponse
from .models import DATABASE
from django.http import HttpResponse


def products_view(request):
    if request.method == "GET":
        data = DATABASE

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

        # Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
        # как в приложении app_weather



def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ