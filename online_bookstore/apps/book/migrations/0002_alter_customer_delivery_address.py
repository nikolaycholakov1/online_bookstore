# Generated by Django 4.2.3 on 2023-07-29 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='delivery_address',
            field=models.CharField(blank=True, null=True),
        ),
    ]