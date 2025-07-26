from django.db import models

from shops.models import Shop

# Create your models here.

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="categories")

    class Meta:
        unique_together = ('name', 'shop')  # optional, prevents duplicate categories per shop




class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    calories = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="menu/images/", blank=True, null=True)
    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)



