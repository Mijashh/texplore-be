from django.contrib import admin

from .models import Product, Category, Cart, CartItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)


# Register your models here.
