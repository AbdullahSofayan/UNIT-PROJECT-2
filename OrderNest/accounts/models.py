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
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)

    # This field is only for shop admins
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash password only if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

