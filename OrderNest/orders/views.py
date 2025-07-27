from django.shortcuts import get_object_or_404, redirect, render
from menu.models import MenuItem
from django.http import HttpRequest
from shops.models import Shop 



def add_to_cart_view(request: HttpRequest, shop_id, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)
        quantity = int(request.POST.get("quantity", 1))

        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        if str(item_id) in shop_cart:
            shop_cart[str(item_id)] += quantity
        else:
            shop_cart[str(item_id)] = quantity

        cart[str(shop_id)] = shop_cart
        request.session["cart"] = cart
        request.session.modified = True

    # Redirect to the page the user came from
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    else:
        return redirect('menu:menu_view', shop_id=shop_id)




def cart_view(request: HttpRequest, shop_id):
    cart = request.session.get("cart", {})
    shop_carts = []
    shop = None  # ✅ Make sure it's always defined

    shop_cart_data = cart.get(str(shop_id))
    if shop_cart_data:
        try:
            shop = Shop.objects.get(pk=shop_id)
            items = []
            total = 0
            for item_id, quantity in shop_cart_data.items():
                try:
                    item = MenuItem.objects.get(pk=item_id)
                    item.quantity = quantity
                    item.total_price = item.price * quantity
                    items.append(item)
                    total += item.total_price
                except MenuItem.DoesNotExist:
                    continue

            shop_carts.append({
                "shop": shop,
                "items": items,
                "total": total
            })
        except Shop.DoesNotExist:
            pass

    return render(request, "cart_page.html", {
        "shop_carts": shop_carts,
        "shop": shop,  # ✅ Now safe to access even if None
    })






def remove_from_cart_view(request: HttpRequest, shop_id, item_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        if str(item_id) in shop_cart:
            if shop_cart[str(item_id)] > 1:
                shop_cart[str(item_id)] -= 1  # Decrease quantity by 1
            else:
                del shop_cart[str(item_id)]  # Remove if quantity reaches 0

        # If the shop_cart is now empty, remove the shop entry
        if shop_cart:
            cart[str(shop_id)] = shop_cart
        else:
            cart.pop(str(shop_id), None)

        request.session["cart"] = cart
        request.session.modified = True

    return redirect('orders:cart_view', shop_id=shop_id)



