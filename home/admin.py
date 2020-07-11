from django.contrib import admin
from .models import Slide, Category, Product, Images, OrderItem, Order, Coupon, Refund, Address

# Register your models here.
admin.site.register((Slide, Category, Product, Images, OrderItem, Order, Coupon, Refund, Address))


