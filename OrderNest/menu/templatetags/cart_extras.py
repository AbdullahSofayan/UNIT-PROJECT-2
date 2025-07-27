from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_shop_cart_count(context, shop_id):
    request = context.get("request")

    if not request or not hasattr(request, "session"):
        return 0

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        return 0

    shop_cart = cart.get(str(shop_id), {})
    if not isinstance(shop_cart, dict):
        return 0

    count = 0
    for item_data in shop_cart.values():
        if isinstance(item_data, dict):
            count += item_data.get("quantity", 0)

    return count
