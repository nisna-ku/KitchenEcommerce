# Generated by Django 5.1.3 on 2025-02-26 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0005_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
