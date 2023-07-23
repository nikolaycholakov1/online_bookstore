# models.py in the 'book' app

from django.core import validators
from django.db import models


class Book(models.Model):
    TITLE_MAX_LEN = 200
    TITLE_MIN_LEN = 2

    AUTHOR_NAME_MAX_LEN = 100
    AUTHOR_NAME_MIN_LEN = 2

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=[
            validators.MinLengthValidator(TITLE_MIN_LEN),
        ],
        null=False,
        blank=False,
    )
    author = models.CharField(
        max_length=AUTHOR_NAME_MAX_LEN,
        validators=[
            validators.MinLengthValidator(AUTHOR_NAME_MIN_LEN),
        ],
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=False,
    )



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
