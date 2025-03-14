from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'price', 'stock', 'category', 'image']
    list_filter = ['category', 'brand']
    search_fields = ['name', 'brand', 'category']
    list_editable = ['price']

admin.site.register(Product, ProductAdmin)