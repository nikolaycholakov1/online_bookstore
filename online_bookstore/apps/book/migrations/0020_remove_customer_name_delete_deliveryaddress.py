# Generated by Django 4.2.3 on 2023-08-09 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_remove_customer_site_color_theme_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
        migrations.DeleteModel(
            name='DeliveryAddress',
        ),
    ]
