from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from shops.models import Shop
from .models import MenuCategory
from .forms import MenuItemForm, MenuCategoryForm, MenuItem
from django.contrib import messages

# Create your views here.

def menu_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    categories = MenuCategory.objects.filter(shop=shop).prefetch_related("items")  


    return render(request, "menu_page.html", {
        "shop": shop,
        "categories": categories,
    })


def manage_menu_view(request: HttpRequest, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    categories = MenuCategory.objects.filter(shop=shop).prefetch_related("items")

    return render(request, "manage_menu.html", {
        "shop": shop,
        "categories": categories,
    })

def add_menu_item_view(request: HttpRequest, shop_id, category_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    category = get_object_or_404(MenuCategory, pk=category_id, shop=shop)

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = category
            item.save()
            return redirect('menu:manage_menu', shop_id=shop.id)
    else:
        form = MenuItemForm()

    return render(request, 'add_menu_item.html', {
        'form': form,
        'shop': shop,
        'category': category
    })

def add_category_view(request, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)

    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.shop = shop
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('menu:manage_menu', shop_id=shop.id)
    else:
        form = MenuCategoryForm()

    return render(request, 'add_category.html', {
        'form': form,
        'shop': shop
    })

def delete_menu_item_view(request, shop_id, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('menu:manage_menu', shop_id=shop_id)


def delete_menu_category_view(request, shop_id, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    category.delete()
    return redirect('menu:manage_menu', shop_id=shop_id)

def update_menu_item_view(request: HttpRequest, shop_id, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    shop = get_object_or_404(Shop, pk=shop_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.category = item.category 
            updated_item.save()
            return redirect("menu:manage_menu", shop_id=shop_id)
    else:
        form = MenuItemForm(instance=item)

    return render(request, "update_item.html", {'shop':shop, 'item':item, 'form':form})



