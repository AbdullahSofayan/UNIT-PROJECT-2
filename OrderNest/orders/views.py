from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Cart, CartItem, Order, OrderItem, OrderItemOption
from menu.models import MenuItem, MenuItemOption
from django.http import HttpRequest
from shops.models import Shop 
from .forms import CheckoutForm
from accounts.models import Address, User

def get_or_create_cart(user, shop_id):
    cart, created = Cart.objects.get_or_create(user=user, shop_id=shop_id)
    return cart


def add_to_cart_view(request: HttpRequest, shop_id, item_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        cart = get_or_create_cart(user=user, shop_id=shop_id)

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

        cart_item = CartItem.objects.create(
            cart=cart,
            item=item,
            quantity=quantity,
            options=options,
            base_price=item.price,
            total_price=total_price * quantity
        )

    return redirect("menu:menu_view", shop_id=shop_id)


def add_existing_to_cart_view(request: HttpRequest, shop_id, cart_item_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    cart = get_object_or_404(Cart, user=user, shop_id=shop_id)
    item = get_object_or_404(CartItem, cart=cart, id=cart_item_id)

    if request.method == "POST":
        # Calculate unit price
        unit_price = item.base_price
        for opt in item.options:
            unit_price += Decimal(str(opt["extra_price"]))

        # Update quantity and price
        item.quantity += 1
        item.total_price += unit_price
        item.save()

    return redirect("orders:cart_view", shop_id=shop_id)

from django.views.decorators.http import require_POST

@require_POST
def delete_from_cart_view(request: HttpRequest, shop_id, item_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    cart = get_object_or_404(Cart, user=user, shop_id=shop_id)
    item = get_object_or_404(CartItem, cart=cart, id=item_id)

    item.delete()

    return redirect('orders:cart_view', shop_id=shop_id)


def cart_view(request: HttpRequest, shop_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)

    cart = Cart.objects.filter(user=user, shop_id=shop_id).first()
    items = []
    total = 0
    shop = get_object_or_404(Shop, id=shop_id)

    if cart:
        for item in cart.items.all():
            total += item.total_price
        items = cart.items.all()

    return render(request, "cart_page.html", {
        "shop_carts": [{"shop": shop, "items": items, "total": total}],
        "shop": shop,
    })


def remove_from_cart_view(request: HttpRequest, shop_id, item_id):  
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    cart = get_object_or_404(Cart, user=user, shop_id=shop_id)
    item = get_object_or_404(CartItem, cart=cart, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.total_price -= item.base_price + sum(Decimal(str(opt["extra_price"])) for opt in item.options)
        item.save()
    else:
        item.delete()

    return redirect('orders:cart_view', shop_id=shop_id)



def edit_cart_item_view(request, shop_id, item_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    cart = get_object_or_404(Cart, user=user, shop_id=shop_id)
    item = get_object_or_404(CartItem, cart=cart, id=item_id)
    all_options = MenuItemOption.objects.filter(category=item.item.category)

    if request.method == "POST":
        option_ids = request.POST.getlist("options")
        quantity = int(request.POST.get("quantity", 1))

        options = []
        total_price = item.item.price

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

        item.quantity = quantity
        item.options = options
        item.base_price = item.item.price
        item.total_price = total_price * quantity
        item.save()

        return redirect("orders:cart_view", shop_id=shop_id)

    selected_option_ids = [str(opt["id"]) for opt in item.options]

    return render(request, "edit_cart_item.html", {
        "shop_id": shop_id,
        "item": item.item,
        "item_id": item.id,
        "options": all_options,
        "selected_option_ids": selected_option_ids,
        "quantity": item.quantity,
    })



def checkout_view(request, shop_id):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    addresses = user.addresses.all()

    cart = Cart.objects.filter(user=user, shop_id=shop_id).first()
    if not cart:
        return redirect("orders:cart_view", shop_id=shop_id)

    cart_items = []
    total = 0

    for item in cart.items.all():
        subtotal = item.total_price
        total += subtotal
        item.subtotal = subtotal  
        cart_items.append(item)

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        address = get_object_or_404(Address, id=address_id, user=user)

        order = Order.objects.create(
            customer=user,
            shop_id=shop_id,
            address=address,
            total=total,
        )

        for entry in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                item=entry.item,
                quantity=entry.quantity,
                base_price=entry.base_price,
            )
            for opt in entry.options:
                OrderItemOption.objects.create(
                    order_item=order_item,
                    name=opt["name"],
                    extra_price=opt["extra_price"],
                )

        cart.delete()  # clear cart after order
        return redirect("orders:order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "user": user,
        "cart_items": cart_items,
        "total": total,
        "addresses": addresses,
        "shop_id": shop_id,
    })


def order_success(request, order_id):
    return render(request, 'success.html', {"order_id": order_id})
