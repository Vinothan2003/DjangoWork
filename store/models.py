from django.db import models


class Collection(models.Model):
    title = models.CharField(max_length=225)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True,
                                         related_name='+')  # CIRCULAR RELATIONSHIP


class Promotion(models.Model):
    description = models.CharField(max_length=225)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=225)
    # slug = models.SlugField(default="-", null=True)
    slug = models.SlugField()
    description = models.CharField(max_length=225)
    unit_price = models.DecimalField(decimal_places=2, max_digits=6)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)  # ONE-TO-MANY RELATION SHIP
    products = models.ManyToManyField(Promotion)  # MANY-TO-MANY RELATIONSHIP


class Customer(models.Model):
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


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # ONE-TO-MANY RELATION SHIP


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)  # ONE-TO-MANY RELATION SHIP
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # ONE-TO-MANY RELATION SHIP
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # ONE-TO-MANY RELATION SHIP
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ONE-TO-MANY RELATION SHIP
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    zip = models.IntegerField()
