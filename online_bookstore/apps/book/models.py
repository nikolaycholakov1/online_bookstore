# models.py in the 'book' app

from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    author = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
    )
    cover_image = models.ImageField(
        upload_to='book_covers/',
        null=False,
        blank=False,
    )
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
