from django.shortcuts import get_object_or_404, redirect, render
from menu.models import MenuItem
from django.http import HttpRequest
from shops.models import Shop 



def add_to_cart_view(request: HttpRequest, shop_id, item_id):
    if request.method == "POST":
        item = get_object_or_404(MenuItem, id=item_id)

        # Initialize 'cart' in session if not present
        cart = request.session.get("cart", {})

        # Use shop_id as a key for a nested cart
        shop_cart = cart.get(str(shop_id), {})

        if str(item_id) in shop_cart:
            shop_cart[str(item_id)] += 1
        else:
            shop_cart[str(item_id)] = 1

        # Update cart structure
        cart[str(shop_id)] = shop_cart
        request.session["cart"] = cart
        request.session.modified = True

    return redirect('menu:menu_view', shop_id=shop_id)





def cart_view(request: HttpRequest, shop_id):
    cart = request.session.get("cart", {})
    shop_carts = []

    for shop_id, shop_items in cart.items():
        try:
            shop = Shop.objects.get(pk=shop_id)
        except Shop.DoesNotExist:
            continue

        items = []
        total = 0
        for item_id, quantity in shop_items.items():
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
        

    return render(request, "cart_page.html", {
        "shop_carts": shop_carts,
    })





def remove_from_cart_view(request: HttpRequest, shop_id, item_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        if str(item_id) in shop_cart:
            del shop_cart[str(item_id)]

        # If the shop_cart is now empty, remove the shop entry
        if shop_cart:
            cart[str(shop_id)] = shop_cart
        else:
            cart.pop(str(shop_id), None)

        request.session["cart"] = cart
        request.session.modified = True
    

    return redirect('cart_view', shop_id=shop_id)


