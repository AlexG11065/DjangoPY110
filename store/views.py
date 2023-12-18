from django.shortcuts import render

from django.http import JsonResponse
from .models import DATABASE
from django.http import HttpResponse, HttpResponseNotFound, Http404
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


# def products_view(request):
#     if request.method == "GET":
#         products_id = request.GET.get('id')
#         if products_id:
#             if products_id in DATABASE:
#                 return JsonResponse(DATABASE[products_id], json_dumps_params={'ensure_ascii': False,
#                                                                               'indent': 4})
#             else:
#                 return HttpResponseNotFound('Данного продукта нет в базе данных')
#         else:
#             return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
#                                                              'indent': 4})


# def products_page_view(request, page):
#     if request.method == "GET":
#         for data in DATABASE.values():
#             if data['html'] == page:  # если значение переданного параметра совпадает с именем html-файла
#                 with open(f'store/products/{page}.html',
#                           encoding="utf-8") as file:  # открыть файл с помощью контекстного менеджера
#                     content = file.read()  # читаем содержимое файла
#                 return HttpResponse(content)  # возвращает HttpResponse с содержимым html-файла
#
#         return HttpResponse(status=404)

def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', encoding="utf-8") as file:
                        content = file.read()
                        return HttpResponse(content)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as file:
                    cont = file.read()
                    return HttpResponse(cont)

        return HttpResponse(status=404)


def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") in ('true', 'True'):  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)  # Провести фильтрацию с параметрами
            else:
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          False)  # TODO Провести фильтрацию с параметрами
        else:
            data = filtering_category(DATABASE, category_key)  # TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()  # Вызвать ответственную за это действие функцию
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)  # Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)  # Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
