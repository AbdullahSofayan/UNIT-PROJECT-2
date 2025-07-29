from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<int:shop_id>/add-to-cart/<int:item_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('<int:shop_id>/cart/add/<int:cart_item_id>/', views.add_existing_to_cart_view, name='add_existing_to_cart'),

    path('shop/<int:shop_id>/cart/', views.cart_view, name='cart_view'),
    path('<int:shop_id>/cart/remove/<str:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('<int:shop_id>/cart/delete/<int:item_id>/', views.delete_from_cart_view, name='delete_from_cart'),
    path('<int:shop_id>/edit/<str:item_id>/', views.edit_cart_item_view, name='edit_cart_item'),
    path('<int:shop_id>/checkout/', views.checkout_view, name='checkout_view'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('payment/<int:order_id>/', views.payment_view, name='payment_view'),



]