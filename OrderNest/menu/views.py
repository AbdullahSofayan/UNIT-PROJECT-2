from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from shops.models import Shop
from .models import MenuCategory, MenuItemOption
from .forms import MenuItemForm, MenuCategoryForm, MenuItem, MenuItemOptionForm
from django.contrib import messages
from django.views.decorators.http import require_POST

# Create your views here.

def menu_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    categories = MenuCategory.objects.filter(shop=shop).prefetch_related("items")  


    return render(request, "menu_page.html", {
        "shop": shop,
        "categories": categories,
        "quantities": range(1, 11)

    })


def manage_menu_view(request: HttpRequest, shop_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    categories = MenuCategory.objects.filter(shop=shop).prefetch_related("items")

    return render(request, "manage_menu.html", {
        "shop": shop,
        "categories": categories,
    })



def manage_options_view(request, shop_id, category_id):
    shop = get_object_or_404(Shop, id=shop_id)
    category = get_object_or_404(MenuCategory, id=category_id, shop=shop)
    options = MenuItemOption.objects.filter(category=category)

    return render(request, 'manage_options.html', {
        'shop': shop,
        'category': category,
        'options': options,
    })


@require_POST
def update_option(request, shop_id, category_id, option_id):
    option = get_object_or_404(MenuItemOption, id=option_id, category_id=category_id)
    option.name = request.POST.get("name", option.name)
    option.extra_price = request.POST.get("extra_price", option.extra_price)
    option.save()
    return redirect("menu:manage_menu", shop_id=shop_id)

def delete_option(request, shop_id, category_id, option_id):
    option = get_object_or_404(MenuItemOption, id=option_id, category_id=category_id)
    option.delete()
    return redirect("menu:manage_menu", shop_id=shop_id)



def add_menu_item_view(request: HttpRequest, shop_id, category_id):
    shop = get_object_or_404(Shop, pk=shop_id)
    category = get_object_or_404(MenuCategory, pk=category_id, shop=shop)

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, shop=shop)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = category
            item.shop = shop 
            item.save()
            return redirect('menu:manage_menu', shop_id=shop.id)
    else:
        form = MenuItemForm(shop=shop)

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
        form = MenuItemForm(request.POST, request.FILES, instance=item, shop=shop)
        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.category = item.category
            updated_item.shop = shop 
            updated_item.save()
            return redirect("menu:manage_menu", shop_id=shop_id)
    else:
        form = MenuItemForm(instance=item, shop=shop) 


    return render(request, "update_item.html", {'shop': shop, 'item': item, 'form': form})


def update_menu_category_view(request, shop_id, category_id):
    category = get_object_or_404(MenuCategory, pk=category_id, shop_id=shop_id)

    if request.method == "POST":
        new_name = request.POST.get("name", "").strip()
        if new_name:
            category.name = new_name
            category.save()
            messages.success(request, "Category name updated successfully.")
        else:
            messages.error(request, "Category name cannot be empty.")

    return redirect("menu:manage_menu", shop_id=shop_id)


def add_option_to_category(request, shop_id, category_id):
    category = get_object_or_404(MenuCategory, id=category_id)
    shop = get_object_or_404(Shop, pk=shop_id)

    if request.method == "POST":
        form = MenuItemOptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.category = category
            option.save()
            return redirect('menu:manage_menu', shop_id=shop_id)
    else:
        form = MenuItemOptionForm()
    return render(request, 'add_option.html', {'form': form, 'category': category, 'shop': shop})



def item_detail_view(request, shop_id, item_id):
    item = get_object_or_404(MenuItem, id=item_id, category__shop_id=shop_id)
    options = item.category.options.all()
    
    return render(request, 'item_details.html', {
        'item': item,
        'options': options,
        'shop_id': shop_id,
    })
