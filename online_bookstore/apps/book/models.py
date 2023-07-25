# book/models.py

from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class Book(models.Model):
    TITLE_MAX_LEN = 200
    TITLE_MIN_LEN = 2

    AUTHOR_NAME_MAX_LEN = 100
    AUTHOR_NAME_MIN_LEN = 2

    CATEGORIES = (
        ("Children's literature", "Children's literature"),
        ("Fiction", "Fiction"),
        ("Historical Fiction", "Historical Fiction"),
        ("Science fiction", "Science fiction"),
        ("Mystery", "Mystery"),
        ("Memoir", "Memoir"),
        ("Thriller", "Thriller"),
        ("Humor", "Humor"),
        ("Romance novel", "Romance novel"),
    )

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        validators=[
            validators.MinLengthValidator(TITLE_MIN_LEN),
        ],
        null=False,
        blank=False,
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORIES,
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


class BookReview(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    review_text = models.TextField(
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
