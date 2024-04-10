from django.contrib import admin
from . models import Product
class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name','price','category','stock', 'updated_at','is_available']
    prepopulated_fields = {"slug":("product_name",)}
admin.site.register(Product, AdminProduct)