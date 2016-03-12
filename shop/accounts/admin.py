from django.contrib import admin

from .models import Customer, Delivery


class CustomerAdmin(admin.ModelAdmin):
    """docstring for CustomerAdmin"""
    def customer_name(obj):
        return "{} {} {}".format(obj.user.first_name, obj.patronymic, obj.user.last_name)

    def customer_joined(obj):
        return obj.user.date_joined

    list_display = ('user', customer_name, 'phone', customer_joined)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')


class DeliveryAdmin(admin.ModelAdmin):
    """docstring for DeliveryAdmin"""
    list_display = ('customer', 'address')
    search_fields = ('address',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Delivery, DeliveryAdmin)
