# Generated by Django 5.1.6 on 2025-02-25 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
    ]
