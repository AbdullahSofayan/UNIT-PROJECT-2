from decimal import Decimal
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Cart, CartItem, Order, OrderItem, OrderItemOption, Payment
from menu.models import MenuItem, MenuItemOption
from django.http import HttpRequest
from shops.models import Branch, Shop 
from .forms import CheckoutForm, PaymentForm
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
    branches = Branch.objects.filter(shop_id=shop_id)

    cart = Cart.objects.filter(user=user, shop_id=shop_id).first()
    if not cart:
        return redirect("orders:cart_view", shop_id=shop_id)

    cart_items = cart.items.all()
    total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        print("check post")

        print("post")
        method = request.POST.get('method')
        address_id = request.POST.get('address_id')
        branch_id = request.POST.get('branch_id')
        print("METHOD:", method)
        print("ADDRESS_ID:", address_id)
        print("BRANCH_ID:", branch_id)
        if method == 'delivery':
            if not address_id:
                messages.error(request, "Please select a delivery address.")
                return redirect('orders:checkout', shop_id=shop_id)
            address = get_object_or_404(Address, id=address_id, user=user)  
            branch = None
        elif method == 'pickup':
            if not branch_id:
                messages.error(request, "Please choose a branch.")
                return redirect('orders:checkout', shop_id=shop_id)
            branch = get_object_or_404(Branch, id=branch_id, shop_id=shop_id)
            address = None
        else:
            messages.error(request, "Please select a delivery method.")
            return redirect('orders:checkout', shop_id=shop_id)



        branch = get_object_or_404(Branch, id=branch_id) if method == "pickup" else None

        order = Order.objects.create(
            customer=user,
            address=address,
            shop_id=shop_id,
            branch=branch,
            method=method,
            customer_name=user.full_name,
            phone=user.phone,
            total=total,
        )



        for entry in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                item=entry.item,
                quantity=entry.quantity,
                base_price=entry.base_price,
                total_price = entry.total_price
            )
            for opt in entry.options:
                option_obj = MenuItemOption.objects.get(id=opt["id"])  
                OrderItemOption.objects.create(
                    order_item=order_item,
                    option=option_obj,
                    extra_price=opt["extra_price"],
                )

        cart.delete()
        return redirect('orders:payment_view', order_id=order.id)


    return render(request, "checkout.html", {
        "user": user,
        "cart_items": cart_items,
        "total": total,
        "addresses": addresses,
        "branches": branches,
        "shop_id": shop_id,
    })




def my_orders_view(request):
    user_id = request.session.get("customer_id")
    if not user_id:
        return redirect("accounts:login_view")

    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(customer=user).order_by("-created_at").prefetch_related("items__options", "items__item", "address", "branch")

    return render(request, "orders_page.html", {
        "orders": orders
    })

def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_id=request.session.get("customer_id"))

    if hasattr(order, 'payment') and order.payment.paid:
        return redirect('orders:my_orders')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method']
            if method == 'card':
                # Simulate card validation
                if not form.cleaned_data['card_number']:
                    form.add_error('card_number', 'Card number is required for credit card payment.')
                else:
                    Payment.objects.create(order=order, method='credit_card', paid=True)
                    order.status = Order.CONFIRMED
                    order.save()
                    return redirect('orders:my_orders')
            elif method == 'cash':
                Payment.objects.create(order=order, method='cash', paid=True)
                order.status = Order.CONFIRMED
                order.save()
                return redirect('orders:my_orders')
    else:
        form = PaymentForm()

    return render(request, 'payment_page.html', {
        'form': form,
        'order': order
    })