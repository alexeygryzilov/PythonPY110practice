from django.urls import path
from .views import wishlist_view
from store.views import products_page_view
#  TODO Импортируйте ваше представление

app_name = 'wishlist'

urlpatterns = [
    path('wishlist/', wishlist_view, name="wishlist_view"),
    path('wishlist/products/<slug:page>.html', products_page_view, name="products_page_view"),
    path('wishlist/products/<int:page>', products_page_view),
]