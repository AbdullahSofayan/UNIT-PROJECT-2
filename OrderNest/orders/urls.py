from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<int:shop_id>/add-to-cart/<int:item_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('shop/<int:shop_id>/cart/', views.cart_view, name='cart_view'),
    path('shop/<int:shop_id>/cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),



]