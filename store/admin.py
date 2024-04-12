from django.contrib import admin
from . models import Product, Variation
class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name','price','category','stock', 'updated_at','is_available']
    prepopulated_fields = {"slug":("product_name",)}
admin.site.register(Product, AdminProduct)

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value', 'is_active']
admin.site.register(Variation, VariationAdmin)