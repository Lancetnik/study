from django.contrib import admin

from . import models


admin.site.register(models.ProductCategory)
admin.site.register(models.Product)
admin.site.register(models.ProductInBusket)
admin.site.register(models.ProductImg)
