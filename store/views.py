from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse
from logic.services import filtering_category


# def products_view(request):
#    if request.method == "GET":
# if id_ := request.GET.get('id'):
#     if data := DATABASE.get(id_):
#         return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
# else:
#     return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
#                                              'indent': 4})
# return HttpResponseNotFound("Данного продукта нет в базе данных")
#        id_ = request.GET.get('id')
#        if not id_:
#            return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
#                                                             'indent': 4})
#        if data := DATABASE.get(id_):
#            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

#        return HttpResponseNotFound("Данного продукта нет в базе данных")

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
                result = [good for good in DATABASE.values() if good['category'] == category_key]
                data = sorted(result, key=lambda x: x[ordering_key], reverse=True)
                #  TODO Провести фильтрацию с параметрами
            else:
                result = [good for good in DATABASE.values() if good['category'] == category_key]
                data = sorted(result, key=lambda x: x[ordering_key])
                #  TODO Провести фильтрацию с параметрами
        else:
            data = [good for good in DATABASE.values() if good['category'] == category_key]
            # TODO Провести фильтрацию с параметрами
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ

        # def products_page_view(request, page):
        #    if request.method == "GET":
        #        for data in DATABASE.values():
        #            if data['html'] == page: # Если значение переданного параметра совпадает именем html файла
        #                with open(f'store/products/{page}.html', encoding='utf-8') as f:
        #                    data = f.read()
        #                return HttpResponse(data)
        #        # TODO 1. Откройте файл open(f'store/products/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
        #        # TODO 2. Прочитайте его содержимое
        # TODO 3. Верните HttpResponse c содержимым html файла

        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', encoding='utf-8') as f:
                        data = f.read()
                    return HttpResponse(data)
            # То, что было ранее для обработки типа slug
        elif isinstance(page, int):
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    data_ = f.read()
                return HttpResponse(data_)
                # 1. Откройте файл open(f'store/products/{data["html"]}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
                # 2. Прочитайте его содержимое
                # 3. Верните HttpResponse c содержимым html файла

        return HttpResponse(status=404)
