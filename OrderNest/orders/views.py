from django.shortcuts import get_object_or_404, redirect, render
from orders.models import OrderItem, OrderItemOption
from menu.models import MenuItem, MenuItemOption
from django.http import HttpRequest
from shops.models import Shop 
from .forms import CheckoutForm
from accounts.models import User


def add_to_cart_view(request: HttpRequest, shop_id, item_id):
    if request.method == "POST":
        # ✅ Safely get or initialize session cart
        cart = request.session.get("cart")
        if not isinstance(cart, dict):
            cart = {}

        shop_cart = cart.get(str(shop_id))
        if not isinstance(shop_cart, dict):
            shop_cart = {}

        from_cart = request.POST.get("from_cart")

        if from_cart:
            # 🔁 Reuse existing item in cart (e.g. increasing from cart page)
            cart_key = str(item_id)
            matching_keys = [key for key in shop_cart if key.startswith(str(item_id) + "-") or key == str(item_id)]
            if matching_keys:
                cart_key = matching_keys[0]
                shop_cart[cart_key]["quantity"] += 1

                unit_price = shop_cart[cart_key]["base_price"]
                for opt in shop_cart[cart_key].get("options", []):
                    unit_price += float(opt.get("extra_price", 0))

                shop_cart[cart_key]["total_price"] += unit_price
        else:
            # 🛒 Adding new item from item detail page
            item = get_object_or_404(MenuItem, id=item_id)
            quantity = int(request.POST.get("quantity", 1))
            option_ids = request.POST.getlist("options")
            options = []
            total_price = item.price

            for option_id in option_ids:
                try:
                    option = MenuItemOption.objects.get(id=option_id)
                    total_price += option.extra_price
                    options.append({
                        "id": option.id,
                        "name": option.name,
                        "extra_price": float(option.extra_price)
                    })
                except MenuItemOption.DoesNotExist:
                    continue

            # 🔑 Key includes options so unique combinations are preserved
            cart_key = f"{item_id}-{'-'.join(option_ids)}" if option_ids else str(item_id)

            if cart_key in shop_cart:
                shop_cart[cart_key]["quantity"] += quantity
                shop_cart[cart_key]["total_price"] += total_price
            else:
                shop_cart[cart_key] = {
                    "item_id": item.id,
                    "quantity": quantity,
                    "options": options,
                    "base_price": float(item.price),
                    "total_price": float(total_price)
                }

        # ✅ Save updated cart
        cart[str(shop_id)] = shop_cart
        request.session["cart"] = cart
        request.session.modified = True

    # 🔙 Redirect to previous page or fallback
    return redirect(request.META.get("HTTP_REFERER", '/menu/'))


def add_existing_to_cart_view(request: HttpRequest, shop_id, cart_key):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        if cart_key in shop_cart:
            item_data = shop_cart[cart_key]
            unit_price = item_data["base_price"]

            for opt in item_data.get("options", []):
                unit_price += float(opt.get("extra_price", 0))

            item_data["quantity"] += 1
            item_data["total_price"] += unit_price

        cart[str(shop_id)] = shop_cart
        request.session["cart"] = cart
        request.session.modified = True

    return redirect('orders:cart_view', shop_id=shop_id)


def delete_from_cart_view(request: HttpRequest, shop_id, item_key):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        if item_key in shop_cart:
            del shop_cart[item_key]

        if shop_cart:
            cart[str(shop_id)] = shop_cart
        else:
            cart.pop(str(shop_id), None)

        request.session["cart"] = cart
        request.session.modified = True

    return redirect('orders:cart_view', shop_id=shop_id)






def cart_view(request: HttpRequest, shop_id):
    cart = request.session.get("cart", {})
    shop_carts = []
    shop = None

    shop_cart_data = cart.get(str(shop_id))
    if shop_cart_data:
        try:
            shop = Shop.objects.get(pk=shop_id)
            items = []
            total = 0

            for key, data in shop_cart_data.items():
                if isinstance(data, dict):  # New format with options
                    item = get_object_or_404(MenuItem, id=data["item_id"])
                    item.quantity = data["quantity"]
                    item.total_price = data["total_price"]  # already includes options
                    item.selected_options = data.get("options", [])
                    item.cart_key = key 

                    items.append(item)
                    total += item.total_price

            shop_carts.append({
                "shop": shop,
                "items": items,
                "total": total
            })
        except Shop.DoesNotExist:
            pass

    return render(request, "cart_page.html", {
        "shop_carts": shop_carts,
        "shop": shop,
    })






def remove_from_cart_view(request: HttpRequest, shop_id, item_key):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        shop_cart = cart.get(str(shop_id), {})

        # Match key with or without options
        matching_keys = [key for key in shop_cart.keys() if key.startswith(str(item_key) + "-") or key == str(item_key)]

        for key in matching_keys:
            item_data = shop_cart.get(key)

            if isinstance(item_data, dict):
                if item_data["quantity"] > 1:
                    # Get the unit price: base + all options
                    unit_price = item_data["base_price"]
                    for opt in item_data.get("options", []):
                        unit_price += float(opt.get("extra_price", 0))

                    # Decrease quantity and adjust total
                    item_data["quantity"] -= 1
                    item_data["total_price"] -= unit_price
                else:
                    del shop_cart[key]
                break

        # Remove shop entry if empty
        if shop_cart:
            cart[str(shop_id)] = shop_cart
        else:
            cart.pop(str(shop_id), None)

        request.session["cart"] = cart
        request.session.modified = True

    return redirect('orders:cart_view', shop_id=shop_id)






def edit_cart_item_view(request, shop_id, cart_key):
    cart = request.session.get("cart", {})
    shop_cart = cart.get(str(shop_id), {})
    item_data = shop_cart.get(cart_key)

    if not item_data:
        return redirect('orders:cart_view', shop_id=shop_id)

    item = get_object_or_404(MenuItem, id=item_data["item_id"])
    all_options = MenuItemOption.objects.filter(category=item.category)


    if request.method == "POST":
        # Get new option IDs and quantity
        option_ids = request.POST.getlist("options")
        quantity = int(request.POST.get("quantity", 1))

        options = []
        total_price = item.price

        for option_id in option_ids:
            try:
                option = MenuItemOption.objects.get(id=option_id)
                total_price += option.extra_price
                options.append({
                    "id": option.id,
                    "name": option.name,
                    "extra_price": float(option.extra_price),
                })
            except MenuItemOption.DoesNotExist:
                continue

        new_cart_key = f"{item.id}-{'-'.join(option_ids)}" if option_ids else str(item.id)

        # Remove old entry
        if cart_key in shop_cart:
            del shop_cart[cart_key]

        # Update with new values
        shop_cart[new_cart_key] = {
            "item_id": item.id,
            "quantity": quantity,
            "options": options,
            "base_price": float(item.price),
            "total_price": float(total_price * quantity),
        }

        cart[str(shop_id)] = shop_cart
        request.session["cart"] = cart
        request.session.modified = True

        return redirect("orders:cart_view", shop_id=shop_id)

    selected_option_ids = [str(opt["id"]) for opt in item_data.get("options", [])]

    return render(request, "edit_cart_item.html", {
        "shop_id": shop_id,
        "cart_key": cart_key,
        "item": item,
        "options": all_options,
        "selected_option_ids": selected_option_ids,
        "quantity": item_data.get("quantity", 1),
    })


def checkout_view(request, shop_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("accounts:login_view")

    customer = get_object_or_404(User, id=customer_id)

    cart = request.session.get("cart", {})
    shop_cart = cart.get(str(shop_id), {})
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer  # استخدم العميل من الجلسة
            order.shop = shop

            # ✅ حساب السعر الكلي
            total = sum(item["total_price"] for item in shop_cart.values())
            order.total = total
            order.save()

            # 🛒 حفظ عناصر الطلب
            for cart_key, item_data in shop_cart.items():
                item = MenuItem.objects.get(id=item_data["item_id"])
                order_item = OrderItem.objects.create(
                    order=order,
                    item=item,
                    quantity=item_data["quantity"],
                    base_price=item_data["base_price"],
                    total_price=item_data["total_price"]
                )

                for opt in item_data.get("options", []):
                    try:
                        option_obj = MenuItemOption.objects.get(id=opt["id"])
                        OrderItemOption.objects.create(
                            order_item=order_item,
                            option=option_obj,
                            extra_price=opt["extra_price"]
                        )
                    except MenuItemOption.DoesNotExist:
                        continue

            # 🧹 حذف السلة
            del cart[str(shop_id)]
            request.session["cart"] = cart
            request.session.modified = True

            return redirect("orders:order_success", order_id=order.id)  # تأكد أن لديك هذا الرابط
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {
        "form": form,
        "shop": shop,
        "shop_id": shop_id
    })

def order_success(request, order_id):
    return render(request, 'success.html', {"order_id": order_id})

