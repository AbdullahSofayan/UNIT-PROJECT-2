from django.db import models
from shops.models import Shop, Branch
from accounts.models import Customer  

ORDER_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('PROCESSING', 'Processing'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
]

DELIVERY_METHOD_CHOICES = [
    ('PICKUP', 'Pickup'),
    ('DELIVERY', 'Delivery'),
]

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES, default='PICKUP')
    address = models.CharField(max_length=255, blank=True)  # only used if delivery
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)



    def get_total_price(self):
        return self.quantity * self.unit_price
