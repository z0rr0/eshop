from django.contrib import admin

from .models import Category, Product, Order


class ProductAdmin(admin.ModelAdmin):
    """docstring for ProductAdmin"""
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'desc')
    list_filter = ('category', 'modified')


class OrderAdmin(admin.ModelAdmin):
    """docstring for OrderAdmin"""
    def order_products(order):
        names = [r.name for r in order.product.all()]
        return "[{}]: {}".format(len(names), ', '.join(names))

    def make_sent(self, request, queryset):
        queryset.update(status=1)

    def make_received(self, request, queryset):
        queryset.update(status=2)

    list_display = ('id', 'status', 'customer', order_products, 'modified')
    search_fields = ('desc',)
    list_filter = ('status', 'modified', 'created')
    actions = ('make_sent', 'make_received')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
