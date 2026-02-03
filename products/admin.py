from django.contrib import admin
from products.models import Facture, Order, OrderItem, Product

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Facture)
