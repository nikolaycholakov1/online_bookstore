# store/models.py

from django.db import models

from online_bookstore.apps.book.models import Book, Customer


class BaseModel(models.Model):
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
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

    def get_total(self):
        total = self.book.price * self.quantity
        return total

    class Meta:
        abstract = True


class Order(models.Model):
    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        Customer,
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

    def total_price(self):
        total = 0
        order_items = self.orderitem_set.all()
        for item in order_items:
            total += item.get_total()
        return total

    def mark_as_shipped(self):
        self.status = 'Shipped'
        self.save()

    def mark_as_delivered(self):
        self.status = 'Delivered'
        self.save()

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )


class Cart(models.Model):
    user = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def total_price(self):
        total = 0
        cart_items = self.cartitem_set.all()
        for item in cart_items:
            total += item.get_total()
        return total

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
