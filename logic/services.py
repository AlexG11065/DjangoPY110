from django.http import JsonResponse
import pprint
import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user


def filtering_category(database: dict,
                       category_key: [int, str],
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных.
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [product for product in database.values() if
                  product['category'] == category_key]  # При помощи фильтрации в
        # list comprehension профильтруйте товары по категории. Или можете использовать
        # обычный цикл или функцию filter

    else:
        result = JsonResponse(database, json_dumps_params={'ensure_ascii': False,
                                                           'indent': 4})  # Трансформируйте database в список
        # словарей
    if ordering_key:
        result.sort(key=lambda x: x[ordering_key],
                    reverse=reverse)  # Проведите сортировку result по ordering_key и параметру reverse
    return result


def view_in_cart(request) -> dict:
    """
    Просматривает содержимое cart.json
    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)
    user = get_user(request).username
    cart = {user: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    if id_product not in cart['products']:  # Проверьте, а существует ли такой товар в корзине, если нет, то перед
        # тем как его добавить - проверьте есть
        if not DATABASE.get(id_product):  # проверка есть ли такой товар в датобазе, чтобы уберечь себя от добавления
            # несуществующего товара.
            return False
        cart['products'][id_product] = 1
        # если в первые, то добовляем.
    else:
        cart['products'][id_product] += 1
        # Если товар существует, то увеличиваем его количество на 1
    with open('cart.json', mode='w', encoding='utf=8') as file:
        # Не забываем записать обновленные данные cart в
        # 'cart.json'
        json.dump(cart_users, file)
    return True


def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    if id_product not in cart['products']:  # Проверьте, а существует ли такой товар в корзине, если нет,
        # то возвращаем False.
        return False
    del cart['products'][id_product]  # Если существует товар, то удаляем ключ 'id_product' у cart['products'].
    with open('cart.json', mode='w', encoding='utf=8') as file:  # Не забываем записать обновленные данные cart в
        # 'cart.json'
        json.dump(cart_users, file)
    return True


def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)
#
# if __name__ == "__main__":
#     # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
#     # Для совпадения выходных значений перед запуском скрипта удаляйте появляющийся файл 'cart.json' в папке
#     print(view_in_cart())  # {'products': {}}
#     print(add_to_cart('1'))  # True
#     print(add_to_cart('0'))  # False
#     print(add_to_cart('1'))  # True
#     print(add_to_cart('2'))  # True
#     print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
#     print(remove_from_cart('0'))  # False
#     print(remove_from_cart('1'))  # True
#     print(view_in_cart())  # {'products': {'2': 1}}

# Предыдущий код, что был для проверки filtering_category закомментируйте
# if __name__ == "__main__":
#     from store.models import DATABASE
#
#     test = [
#         {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
#          'price_after': 500.0,
#          'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
#          'rating': 5.0, 'review': 200, 'sold_value': 700,
#          'weight_in_stock': 400,
#          'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
#          'html': 'strawberry'},
#
#         {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
#          'price_after': 130.0,
#          'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
#          'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
#          'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
#          'html': 'apple'}
#     ]
#
#     print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True
#     # pprint.pprint(filtering_category(DATABASE, 'Фрукты', 'price_after'))
