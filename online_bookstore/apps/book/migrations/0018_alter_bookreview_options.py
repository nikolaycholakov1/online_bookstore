# Generated by Django 4.2.3 on 2023-08-04 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_customer_site_color_theme'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookreview',
            options={'ordering': ['-created_at']},
        ),
    ]
