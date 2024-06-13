from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from uuid import uuid4


class Collection(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    title = models.CharField(max_length=225)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True,
                                         related_name='+')  # CIRCULAR RELATIONSHIP

    def __str__(self):
        return self.title

    """class Meta:
        ordering = ['title']"""


class Promotion(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    description = models.CharField(max_length=225)
    discount = models.FloatField()


class Product(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    title = models.CharField(max_length=225)
    # slug = models.SlugField(default="-", null=True)
    slug = models.SlugField()
    description = models.CharField(max_length=225, null=True, blank=True)
    unit_price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(Decimal(1.00))]
        # validators = [MinValueValidator(1, message='')] --> if custom message required
    )
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,
                                   related_name='products')  # ONE-TO-MANY RELATION SHIP
    promotion = models.ManyToManyField(Promotion, blank=True)  # MANY-TO-MANY RELATIONSHIP

    """class Meta:
        ordering = ['title']"""

    def __str__(self):
        return self.title


class Customer(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=220)
    last_name = models.CharField(max_length=220)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=30, null=True)
    phone_no = models.CharField(max_length=220)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Order(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField()
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')  # ONE-TO-MANY RELATION SHIP

    def __str__(self):
        return self.payment_status


class OrderItem(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    order = models.ForeignKey(Order, on_delete=models.PROTECT)  # ONE-TO-MANY RELATION SHIP
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='orderitems')  # ONE-TO-MANY RELATION SHIP
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    id = models.UUIDField(primary_key=True, default=uuid4)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # ONE-TO-MANY RELATION SHIP
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ONE-TO-MANY RELATION SHIP
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Address(models.Model):  # INTERNAL RESOURCE REPRESENTATION
    zip = models.IntegerField()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
