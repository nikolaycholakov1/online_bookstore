# book/models.py

from django.contrib.auth.models import User, AbstractUser
from django.core import validators
from django.db import models


class Customer(AbstractUser):
    NAME_MAX_LEN = 30
    NAME_MIN_LEN = 2

    EMAIL_MAX_LEN = 50
    DELIVERY_ADDRESS_MIN_LEN = 10
    DELIVERY_ADDRESS_MAX_LEN = 250

    MIN_AGE_VALUE = 1
    MAX_AGE_VALUE = 150

    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        unique=True,
        null=True,
        validators=[
            validators.EmailValidator()
        ]
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            validators.MinValueValidator(MIN_AGE_VALUE),
            validators.MaxValueValidator(MAX_AGE_VALUE),
        ],
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    delivery_address = models.CharField(
        max_length=DELIVERY_ADDRESS_MAX_LEN,
        null=True,
        blank=True,
        validators=[
            validators.MinLengthValidator(DELIVERY_ADDRESS_MIN_LEN),
        ],
    )

    def __str__(self):
        return self.username

    def get_total_comments(self):
        return self.bookreview_set.count()


class Book(models.Model):
    TITLE_MAX_LEN = 200
    TITLE_MIN_LEN = 2

    AUTHOR_NAME_MAX_LEN = 100
    AUTHOR_NAME_MIN_LEN = 2

    CATEGORIES = (
        ("Children's literature", "Children's literature"),
        ("Fiction", "Fiction"),
        ("Historical Fiction", "Historical Fiction"),
        ("Science Fiction", "Science Fiction"),
        ("Mystery", "Mystery"),
        ("Memoir", "Memoir"),
        ("Thriller", "Thriller"),
        ("Humor", "Humor"),
        ("Romance novel", "Romance novel"),
        ("Non-fiction", "Non-fiction"),
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

    pages = models.IntegerField(
        default=1,
        null=False,
        blank=False,
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        default=0,
    )
    cover_image = models.ImageField(
        upload_to='media/book_covers/',
        null=False,
        blank=False,
    )
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class BookReview(models.Model):
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        'book.Customer',
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
        return f"Review by {self.user.username} for {self.book.title}"

    # For sorting the reviews
    class Meta:
        ordering = ['-created_at']
