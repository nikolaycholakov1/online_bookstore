# Generated by Django 4.2.3 on 2023-08-09 23:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0021_remove_customer_delivery_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='delivery_address',
            field=models.CharField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]
