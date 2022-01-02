from django.contrib import admin
from .models import Suppliers, Destinations, Products, Labels


admin.site.register(Suppliers)
admin.site.register(Destinations)
admin.site.register(Products)
admin.site.register(Labels)