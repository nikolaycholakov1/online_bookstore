# book/models.py

from django.contrib.auth.models import User, AbstractUser
from django.core import validators
from django.db import models


class Customer(AbstractUser):
    NAME_MAX_LEN = 30
    EMAIL_MAX_LEN = 50

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        null=True,
    )
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
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    delivery_address = models.CharField(
        null=True,
        blank=True,
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

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
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
        return f"{self.user.username} - {self.book.title}"


class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        'book.Customer',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_date = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='Pending'
    )

    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if not item.book.digital_copy:
                shipping = True
                break
        return shipping

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    @property
    def get_total(self):
        total = self.book.price * self.quantity
        return total


class DeliveryAddress(models.Model):
    COUNTRY_MAX_LEN = 100
    CITY_MAX_LEN = 30
    ADDRESS_MAX_LEN = 200
    ZIP_CODE_MAX_LEN = 9
    SHIPPING_CHOICES = (
        ('By courier', 'By courier'),
        ('From courier office', 'From courier office'),
        ('Supplier', 'Supplier'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    country = models.CharField(
        max_length=COUNTRY_MAX_LEN,
        null=True,
    )

    city = models.CharField(
        max_length=CITY_MAX_LEN,
        null=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LEN,
        null=True,
    )
    zip_code = models.CharField(
        max_length=ZIP_CODE_MAX_LEN,
        null=True,
    )

    shipping_method = models.CharField(
        choices=SHIPPING_CHOICES,
        default='By courier',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.address
