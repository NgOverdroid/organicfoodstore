from django.contrib import admin
from .models import Category, Origin, Customer, Order, Product
# Register your models here.
admin.site.register(Category)
admin.site.register(Origin)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
