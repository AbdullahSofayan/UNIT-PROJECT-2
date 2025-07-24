from django.db import models

from shops.models import Shop

# Create your models here.

class MenuCategory(models.Model):

    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="categories")

class MenuItem(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.PositiveBigIntegerField(blank=True, null=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name="items")
