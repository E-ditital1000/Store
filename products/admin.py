from django.contrib import admin
from .models import Product, Offer, Elvis, Order, Categorie

# Register your models here.
admin.site.register(Product)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Elvis)
admin.site.register(Categorie)

