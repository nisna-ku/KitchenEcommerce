# Generated by Django 5.1.6 on 2025-03-25 05:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0016_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number_1', models.CharField(max_length=15)),
                ('phone_number_2', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
