from django.db import models
from menu.models import MenuItem, MenuItemOption
from shops.models import Shop, Branch
from accounts.models import User, Address

class Order(models.Model):
    DELIVERY = 'delivery'
    PICKUP = 'pickup'
    METHOD_CHOICES = [
        (DELIVERY, 'Delivery'),
        (PICKUP, 'Pickup')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name="options", on_delete=models.CASCADE)
    option = models.ForeignKey(MenuItemOption, on_delete=models.CASCADE)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey("shops.Shop", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    options = models.JSONField(default=list)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)