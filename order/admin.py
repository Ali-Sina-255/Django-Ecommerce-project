from django.contrib import admin
from . models import Payment, Order, OrderProduct

admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Order)