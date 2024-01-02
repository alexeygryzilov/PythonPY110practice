from django.shortcuts import render
from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.shortcuts import render, redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


#def wishlist_view(request):
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
            product[
                'quantity'] = quantity  # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product[
                "price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            products.append(product)  # 3. добавьте product в список products

        return render(request, "wishlist/wishlist.html", context={"products": products})

