from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.shortcuts import get_list_or_404
from users.models import CustomUser
from django.db import models
from django.urls import reverse
from django.conf import settings
from django_extensions.db.fields import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = TextField(blank=True,null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="image/")

    def get_absolute_url(self):
        return reverse('home')
    

class Comment(models.Model):
    comment = models.TextField(max_length=100, null=False, blank=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    date = models.DateField(max_length=50)
    time = models.TimeField(max_length=50)
    facility = models.CharField(max_length=50)



CATEGORY_CHOICES = (
    ('W','和菓子'),
    ('S','精肉'),
    ('K','海産物')

)
LABEL_CHOICES = (
    ('NEW','NEW'),
    ('HOT','HOT'),
)

BOOT_CHOICES = (
    ('warning', 'warning'),
    ('danger', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10)
    boot = models.CharField(choices=BOOT_CHOICES, max_length=10)
    slug = models.SlugField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    image = models.ImageField(null=True, blank=True, upload_to="image/")


    def get_absolute_url(self):
        return reverse('product', kwargs={
            'slug': self.slug,
        })
    
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug,
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug,
        })

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.title} - {self.quantity}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total =0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

PAYMENT_CHOICES = (
    ('C', '現金'),
    ('P', 'ペイパル'),
)

class BillingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    payment_option = models.CharField(max_length=1, choices=PAYMENT_CHOICES)

    def __str__(self):
        return self.user.username

class Compelete(models.Model):
    product = models.ForeignKey(Order,on_delete=models.CASCADE)