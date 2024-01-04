from django.shortcuts import render
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from store.models import DATABASE


# def wishlist_view(request):
#    if request.method == "GET":
#        return render(request,
#                      'wishlist/wishlist.html')  # TODO прописать отображение избранного. Путь до HTML - wishlist/wishlist.html


@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
        products = []  # Список продуктов
        for product_id in data['products']:
            product = DATABASE[
                product_id]  # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
#            product['quantity'] = 1#quantity  # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
#            product[
#                "price_total"] = f"{1 * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            products.append(product)  # 3. добавьте product в список products

        return render(request, "wishlist/wishlist.html", context={"products": products})


@login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = add_to_wishlist(request,
                                 id_product)  # TODO вызовите обработчик из services.py добавляющий продукт в избранное
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={
                                    'ensure_ascii': False})  # TODO верните JsonResponse с ключом "answer" и значением "Продукт успешно добавлен в избранное"

        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404,
                                json_dumps_params={'ensure_ascii': False}) # TODO верните JsonResponse с ключом "answer" и значением "Неудачное добавление в избранное" и параметром status=404

#@login_required(login_url='login:login_view')
def wishlist_del_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO вызовите обработчик из services.py удаляющий продукт из избранного
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"},
                                json_dumps_params={
                                    'ensure_ascii': False}) # TODO верните JsonResponse с ключом "answer" и значением "Продукт успешно удалён из избранного"

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404,
                                json_dumps_params={'ensure_ascii': False})   # TODO верните JsonResponse с ключом "answer" и значением "Неудачное удаление из избранного" и параметром status=404

@login_required(login_url='login:login_view')
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        current_user = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(request)[current_user]  # TODO получите данные о списке товаров в избранном у пользователя
        if data:
            return JsonResponse(data, json_dumps_params={'ensure_ascii':False, 'indent':4})# TODO верните JsonResponse c data

        return JsonResponse({"answer": "пользователь не авторизован"}, status=404,
                                json_dumps_params={'ensure_ascii': False})   # TODO верните JsonResponse с ключом "answer" и значением "Пользователь не авторизирован" и параметром status=404

#@login_required(login_url='login:login_view')
def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("wishlist:wishlist_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из избранного")
