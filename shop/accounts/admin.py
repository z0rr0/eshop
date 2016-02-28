from django.contrib import admin

from .models import Customer, Delivery

# class CustomerAdmin(admin.ModelAdmin):
#     """admin class for CustomerAdmin"""
#     list_display = ('user', 'phone',)
#     search_fields = ('user', 'extension')
#     list_filter = ('extension',)

admin.site.register(Customer)
admin.site.register(Delivery)
