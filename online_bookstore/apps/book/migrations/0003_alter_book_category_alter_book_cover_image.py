# Generated by Django 4.2.3 on 2023-07-29 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_customer_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[("Children's literature", "Children's literature"), ('Fiction', 'Fiction'), ('Historical Fiction', 'Historical Fiction'), ('Science fiction', 'Science fiction'), ('Mystery', 'Mystery'), ('Memoir', 'Memoir'), ('Thriller', 'Thriller'), ('Humor', 'Humor'), ('Romance novel', 'Romance novel'), ('Non-fiction', 'Non-fiction')], max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(upload_to='media/book_covers/'),
        ),
    ]
