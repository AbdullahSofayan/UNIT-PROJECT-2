from django.db import models
from django.contrib.auth.hashers import make_password
from shops.models import Shop

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Shop Admin'),
        ('customer', 'Customer'),
    ]

    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True  # So Django doesn't create a table for this model

    def save(self, *args, **kwargs):
        # Only hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Customer(User):
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True)

class ShopAdmin(User):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
