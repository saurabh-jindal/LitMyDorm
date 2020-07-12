from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

PRODUCT_CHOICES = (
    ('L', 'latest'),
    ('TS', 'top_selling'),
    ('N', 'normal')
)


class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    image = models.ImageField(upload_to='index/images', default='')
    link = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Slide added with captian " + self.caption1

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    desc = models.TextField()
    image = models.ImageField(upload_to='index/images', default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index:category', kwargs={
            'slug': self.slug
        })


class Product(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    short_desc = models.TextField()
    long_desc = models.TextField()
    price = models.FloatField()
    slug = models.SlugField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='index/images', default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    tag = models.CharField(max_length = 20, choices = PRODUCT_CHOICES, default='N')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("index:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("index:remove-from-cart", kwargs={
            'slug': self.slug
        })


class Images(models.Model):
    image = models.ImageField(upload_to='index/images', default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "New Image added for " + self.product.name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return " New Order Added for " + self.product.name + ' of quantity ' + str(self.quantity)

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=150)
    country = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return "New Address Added by " + self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "New payment added by " + self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return "New Coupon added " + self.code + " of rupees " + self.amount


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    is_delivered = models.BooleanField(default=False)
    is_recieved = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return "New Order made by " + self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return 'New refund initiated by ' + self.email
