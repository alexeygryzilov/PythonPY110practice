from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


# def products_view(request):
#    if request.method == "GET":
#        if id_product := request.GET.get('id'):
#           if data := DATABASE.get(id_product):
#                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
#        return HttpResponseNotFound("Данного продукта нет в базе данных")


#    return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False, 'indent': 4})


# def shop_view(request):
#    if request.method == "GET":
#        with open('store/shop.html', encoding="utf-8") as f:
#            data = f.read()  # Читаем HTML файл
#        return HttpResponse(data)  # Отправляем HTML файл как ответ

# def shop_view(request):
#    if request.method == "GET":
#        return render(request, 'store/shop.html', context={"products": DATABASE.values()})

def shop_view(request):
    if request.method == "GET":
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ('true', 'True'):
                data = filtering_category(DATABASE, category_key, ordering_key,
                                          True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html',
                      context={"products": data, "category": category_key})


# def products_page_view(request, page):
#    if request.method == "GET":
#        if isinstance(page, str):
#            for data in DATABASE.values():
#                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
#                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
#                        data = f.read()
#                        return HttpResponse(data)
#            # То, что было ранее для обработки типа slug
#        elif isinstance(page, int):
#            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
#            if data:  # Если по данному page было найдено значение
#                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
#                    data = f.read()
#                    return HttpResponse(data)

#        return HttpResponse(status=404)


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    return render(request, "store/product.html", context={"product": data})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                return render(request, "store/product.html", context={"product": data})

        return HttpResponse(status=404)


def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
            if request.GET.get("reverse") in ('true', 'True'):  # Если в параметрах есть 'ordering' и 'reverse'=True
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
                #  TODO Провести фильтрацию с параметрами
            else:

                data = filtering_category(DATABASE, category_key, ordering_key)
                #  TODO Провести фильтрацию с параметрами
        else:
            data = filtering_category(DATABASE, category_key)
            #  TODO Провести фильтрацию с параметрами
            # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


# def cart_view(request):
#    if request.method == "GET":
#        data = view_in_cart()  # TODO Вызвать ответственную за это действие функцию
#        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                     'indent': 4})

# def cart_view(request):
#    if request.method == "GET":
#        data = view_in_cart()
#        if request.GET.get('format') == 'JSON':
#            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                         'indent': 4})
#        return render(request, "store/cart.html")




@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
#       data = view_in_cart()
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[
                product_id]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product[
                'quantity'] = quantity  # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            products.append(product)  # 3. добавьте product в список products

        return render(request, "store/cart.html", context={"products": products})


@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)  # TODO Вызвать ответственную за это действие функцию
    if result:
        return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                            json_dumps_params={'ensure_ascii': False})

    return JsonResponse({"answer": "Неудачное добавление в корзину"},
                        status=404,
                        json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def coupon_check_view(request, name_coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        if coupon := DATA_COUPON.get(name_coupon):
            return JsonResponse(coupon, json_dumps_params={'ensure_ascii': False})
        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)
        return HttpResponseNotFound("Неверный купон")
        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 80},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        if country in DATA_PRICE and city in DATA_PRICE[country]:
            result = DATA_PRICE[country][city]
            return JsonResponse(result, json_dumps_params={'ensure_ascii': False})
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        elif country in DATA_PRICE and city not in DATA_PRICE[country]:
            result = {}
            result["price"] = DATA_PRICE["Россия"]["fix_price"]
            return JsonResponse(result, json_dumps_params={'ensure_ascii': False})
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        elif country not in DATA_PRICE:
            return HttpResponseNotFound("Неверные данные")
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")


@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")


#def cart_buy_now_view(request, id_product):
#    if request.method == "GET":
#        result = add_to_cart(id_product)
#        if result:
#            return cart_view(request)

#        return HttpResponseNotFound("Неудачное добавление в корзину")


def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")
