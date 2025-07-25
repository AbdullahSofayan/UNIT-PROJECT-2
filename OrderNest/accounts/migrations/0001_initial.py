# Generated by Django 5.2.4 on 2025-07-22 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('admin', 'Shop Admin'), ('customer', 'Customer')], max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('admin', 'Shop Admin'), ('customer', 'Customer')], max_length=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
