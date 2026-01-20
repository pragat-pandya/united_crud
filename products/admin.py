from django.contrib import admin
from .models import Product
# Register your models here.

class ProductManager(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', "created_at")
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ("-created_at",)

admin.site.register(Product, ProductManager)