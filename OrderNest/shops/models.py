from django.db import models

# Create your models here.
class ShopCategory(models.Model):
    name = models.CharField(max_length=50)

class Shop(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ShopCategory, on_delete=models.SET_NULL, null=True, related_name='shops')
    rating = models.FloatField(null=True, blank=True)  




class Branch(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
