# Generated by Django 4.2.3 on 2023-07-30 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_rename_appuser_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[("Children's literature", "Children's literature"), ('Fiction', 'Fiction'), ('Historical Fiction', 'Historical Fiction'), ('Science Fiction', 'Science Fiction'), ('Mystery', 'Mystery'), ('Memoir', 'Memoir'), ('Thriller', 'Thriller'), ('Humor', 'Humor'), ('Romance novel', 'Romance novel'), ('Non-fiction', 'Non-fiction')], max_length=50),
        ),
    ]