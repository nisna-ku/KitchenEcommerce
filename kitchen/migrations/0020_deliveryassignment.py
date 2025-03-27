# Generated by Django 5.1.6 on 2025-03-27 08:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0019_order_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('delivery_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_orders', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_assignment', to='kitchen.order')),
            ],
        ),
    ]
