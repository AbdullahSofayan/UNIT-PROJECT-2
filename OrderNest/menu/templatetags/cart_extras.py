from django import template
from orders.models import Cart, CartItem
from shops.models import Shop
from accounts.models import User

register = template.Library()

@register.simple_tag(takes_context=True)
def get_shop_cart_count(context, shop_id):
    request = context.get("request")
    user_id = request.session.get("customer_id")

    if not user_id:
        return 0

    try:
        cart = Cart.objects.get(user_id=user_id, shop_id=shop_id)
        return sum(item.quantity for item in cart.items.all())
    except Cart.DoesNotExist:
        return 0
