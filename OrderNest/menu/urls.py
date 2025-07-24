from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path("<shop_id>/menu/", views.menu_view, name="menu_view"),
]