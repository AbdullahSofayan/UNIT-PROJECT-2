from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator
from .models import Shop, Branch, ShopCategory

def browse_shops_view(request: HttpRequest):
    category_id = request.GET.get("category")
    search_query = request.GET.get("q","")
    shops = Shop.objects.all()

    if category_id:
        shops = shops.filter(category__id=category_id)

    if search_query:
        shops = shops.filter(name__icontains=search_query)

    paginator = Paginator(shops, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    categories = ShopCategory.objects.values_list("id", "name")

    return render(request,"browse_shops.html",{'shops': page_obj,'page_obj': page_obj,'categories': categories})


def branches_view(request:HttpRequest, shop_id):
    branches = Branch.objects.filter(shop__id=shop_id)
    shop = Shop.objects.get(pk=shop_id)
    return render(request, "branches.html", {'branches':branches, 'shop':shop})