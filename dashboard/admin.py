from django.contrib import admin
from .models import Product, Order
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'quantity', 'category',)
    list_filter= ['category']

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)

