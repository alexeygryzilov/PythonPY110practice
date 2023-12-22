from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import render


#def products_view(request):
#    if request.method == "GET":
#        if id_product := request.GET.get('id'):
#           if data := DATABASE.get(id_product):
#                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
#        return HttpResponseNotFound("Данного продукта нет в базе данных")


#    return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False, 'indent': 4})


#def shop_view(request):
#    if request.method == "GET":
#        with open('store/shop.html', encoding="utf-8") as f:
#            data = f.read()  # Читаем HTML файл
#        return HttpResponse(data)  # Отправляем HTML файл как ответ

def shop_view(request):
    if request.method == "GET":
        return render(request, 'store/shop.html')


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        data = f.read()
                        return HttpResponse(data)
            # То, что было ранее для обработки типа slug
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    data = f.read()
                    return HttpResponse(data)

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


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()  # TODO Вызвать ответственную за это действие функцию
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)  # TODO Вызвать ответственную за это действие функцию
    if result:
        return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                            json_dumps_params={'ensure_ascii': False})

    return JsonResponse({"answer": "Неудачное добавление в корзину"},
                        status=404,
                        json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)  # TODO Вызвать ответственную за это действие функцию
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})
