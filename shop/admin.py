from django.contrib import admin
from shop.models import Product
from djangoToy.custom import CustomModelAdmin
# Register your models here.

@admin.register(Product)
class ProductAdmin(CustomModelAdmin):
    model = Product
    list_display = ['pk','name', 'price', 'owner','author', 'editor','deleter', 'deleted_at']