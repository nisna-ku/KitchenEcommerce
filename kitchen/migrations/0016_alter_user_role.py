# Generated by Django 5.1.6 on 2025-03-25 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0015_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('delivery_person', 'Delivery Person'), ('customer', 'Customer')], default='customer', max_length=20),
        ),
    ]
