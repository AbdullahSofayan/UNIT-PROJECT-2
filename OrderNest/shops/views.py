from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.paginator import Paginator

from OrderNest import settings
from .forms import UpdateShopform, BranchForm
from accounts.models import User
from .models import Shop, Branch, ShopCategory


def browse_shops_view(request: HttpRequest):
    category_id = request.GET.get("category")
    search_query = request.GET.get("search")

    shops = Shop.objects.all()

    if category_id:
        shops = shops.filter(category__id=category_id)

    if search_query:
        shops = shops.filter(name__icontains=search_query)

    total_shops = shops.count()

    paginator = Paginator(shops, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = ShopCategory.objects.values_list("id", "name")

    return render(request, "browse_shops.html", {
        'shops': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'total_shops': total_shops
    })



def branches_view(request:HttpRequest, shop_id):
    branches = Branch.objects.filter(shop__id=shop_id)
    shop = Shop.objects.get(pk=shop_id)
    return render(request, "branches.html", {'branches':branches, 'shop':shop})

def shop_admin_dashboard(request: HttpRequest):
    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("accounts:login_view")

    try:
        admin = User.objects.get(pk=admin_id, role='admin')
    except User.DoesNotExist:
        return redirect("accounts:login_view")

    return render(request, "shop_admin_dashboard.html", {"admin": admin})





def shop_details_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    category_id = shop.category_id
    category = ShopCategory.objects.get(pk=category_id)
    
    return render(request, 'shop_details.html', {'shop':shop, 'category':category})


def shop_update_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)

    if request.method == 'POST':
        form = UpdateShopform(request.POST,instance=shop)
        if form.is_valid():
            form.save()
            return redirect("shops:shop_details_view", shop_id)
    else:
        form = UpdateShopform(instance=shop)

    return render(request, "update_shop.html", {'shop':shop, 'form':form})

def add_branch_view(request: HttpRequest, shop_id):
    shop = Shop.objects.get(pk=shop_id)

    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.shop = shop
            branch.save()
            return redirect('shops:branches_view', shop_id=shop.id)
    else:
        form = BranchForm() 


    return render(request, 'add_branch.html', {'form': form, 'shop': shop ,'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})
