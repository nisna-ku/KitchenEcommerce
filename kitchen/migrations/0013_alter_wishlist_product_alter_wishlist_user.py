# Generated by Django 5.1.6 on 2025-03-05 10:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0012_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(to='kitchen.product'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
