from django import template

register = template.Library()

@register.filter
def get_shop_cart_count(cart, shop_id):
    shop_cart = cart.get(str(shop_id), {}) if cart else {}
    return sum(shop_cart.values())

@register.filter
def to_range(start, end):
    return range(start, end + 1)
