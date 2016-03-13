from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Customer's account"""
    user = models.OneToOneField(User)
    patronymic = models.CharField(max_length=255, verbose_name='patronymic', help_text="user's patronymic")
    phone = models.CharField(max_length=20, verbose_name='phone', help_text="user's phone number")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['id']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Delivery(models.Model):
    """Customers' delivery info"""
    customer =  models.ForeignKey(Customer, verbose_name='customer', on_delete=models.CASCADE)
    address = models.TextField(verbose_name='address', help_text='delivery address')
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "{} delivery".format(self.customer)

    def short(self):
        if len(self.address) > 64:
            return self.address[:64] + "..."
        return self.address

    class Meta:
        ordering = ['address']
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
