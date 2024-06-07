from django.contrib import admin
from store import models


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'featured_product']  # to display the specified fields

    class Meta:
        model = models.Collection  # to show which model


@admin.register(models.Product)  # using annotation to register
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 15

    # ordering = ['title']

    # or

    # @admin.display(ordering="title")
    def inventory_status(self, product):
        if product.inventory < 30:
            return 'Low'
        return 'Ok'

    class Meta:
        model = models.Product


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name']

    class Meta:
        model = models.Customer

# admin.site.register(models.Collection, CollectionAdmin)
# admin.site.register(models.Product, ProductAdmin) # using method to register
