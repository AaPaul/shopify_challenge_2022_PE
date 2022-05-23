from django.contrib import admin

# Register your models here.
from .models import City, Inventory, Warehouse

admin.site.register(Inventory)
admin.site.register(Warehouse)
admin.site.register(City)