# Generated by Django 5.2.4 on 2025-07-24 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_menucategory_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
