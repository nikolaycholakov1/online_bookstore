# Generated by Django 4.2.3 on 2023-08-04 15:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_alter_customer_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='delivery_address',
            field=models.CharField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(10)]),
        ),
    ]