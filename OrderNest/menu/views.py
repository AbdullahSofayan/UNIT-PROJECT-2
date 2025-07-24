from django.shortcuts import render, redirect
from django.http import HttpRequest
from shops.models import Shop
from .models import MenuCategory
# Create your views here.
def menu_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    categories = MenuCategory.objects.filter(shop=shop).prefetch_related("items")  


    return render(request, "menu_page.html", {
        "shop": shop,
        "categories": categories,
    })
