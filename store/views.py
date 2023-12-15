from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE
from django.http import HttpResponse


def products_view(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:
            data = DATABASE.get(id_)
            if data:
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

            return HttpResponseNotFound("Данного продукта нет в базе данных")

    return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ
