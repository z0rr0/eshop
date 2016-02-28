from django.db import models
from django.conf import settings


class Category(models.Model):
    """Products' category"""
    name = models.CharField(max_length=200, verbose_name='name', help_text='category name', unique=True)
    desc = models.TextField(verbose_name='description', help_text='category description')
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """Products class"""
    name = models.CharField(max_length=200, verbose_name='name', help_text='product name')
    category = models.ForeignKey(Category, verbose_name='category', help_text="product's category")
    price = models.FloatField(verbose_name='price', help_text="product's price")
    image = models.ImageField(upload_to=settings.IMAGE_DIR, verbose_name='image', help_text="product's image")
    desc = models.TextField(verbose_name='description', help_text="product's description")
    modified = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    """Orders info"""
    customer = models.ForeignKey('accounts.Customer', verbose_name='customer')
    product = models.ManyToManyField(Product, verbose_name='Product')
    desc = models.TextField(verbose_name='description', help_text="order's description", blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return "Order-{}".format(self.id)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
