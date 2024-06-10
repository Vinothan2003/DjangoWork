from django.contrib import admin, messages
from django.db.models import Count, Value
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.contrib.contenttypes.admin import GenericTabularInline

from store import models
# from tags.models import TaggedItem --> see store custom


# Register your models here.

@admin.register(models.Collection)  # using annotation to register
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'featured_product', 'product_count']  # to display the specified fields
    search_fields = ['title']

    # ordering = ['product_count']

    @admin.display(ordering='product_count', description='product_count')
    def product_count(self, collection):
        # reverse('admin : app_model_page')
        urls = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
        })
        )
        return format_html('<a href = "{}"> {} </a>',
                           urls,
                           collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count('product'))  # overriding the queryset

    class Meta:
        model = models.Collection  # to show which model


class InventoryFilter(admin.SimpleListFilter):  # custom filter
    title = 'Inventory'
    parameter_name = 'inventory'

    # Define the ranges as class variables
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    LOW_RANGE = 10
    MEDIUM_RANGE_START = 10
    MEDIUM_RANGE_END = 50
    HIGH_RANGE = 50

    def lookups(self, request, model_admin):
        # Use the variables to create filter options
        return [
            (self.LOW, f'Low (< {self.LOW_RANGE})'),
            (self.MEDIUM, f'Medium ({self.MEDIUM_RANGE_START}-{self.MEDIUM_RANGE_END})'),
            (self.HIGH, f'High (> {self.HIGH_RANGE})')
        ]

    def queryset(self, request, queryset):
        # Apply the filtering logic using the variables
        if self.value() == self.LOW:
            return queryset.filter(inventory__lt=self.LOW_RANGE)
        if self.value() == self.MEDIUM:
            return queryset.filter(inventory__gte=self.MEDIUM_RANGE_START, inventory__lte=self.MEDIUM_RANGE_END)
        if self.value() == self.HIGH:
            return queryset.filter(inventory__gt=self.HIGH_RANGE)
        return queryset


"""# generic tabular inline
class TagInline(GenericTabularInline):
    model = TaggedItem                       # ---> see store_Custom
    autocomplete_fields = ['tag']
    extra = 0
    min_num = 1
    max_num = 10"""


@admin.register(models.Product)  # using annotation to register
class ProductAdmin(admin.ModelAdmin):
    # exclude = ['promotion'] --> exclude the field
    # readonly_fields = ['promotion'] --> read only filed
    # fields = ['title', 'slug'] --> include the field
    autocomplete_fields = ['collection']  # --> for completion have to include search_field in collection admin
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    # inlines = [TagInline]  --> see store_custom
    list_display = ['id', 'title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 15
    list_filter = ['collection', 'last_update', InventoryFilter]  # --> filter
    search_fields = ['id']

    # list_select_related = ['collection'] --> same as query.select_related()

    # ordering = ['inventory']

    # or

    # @admin.display(ordering="title")
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    """def collection_title(self, product): --> for specified field
        return product.collection.title"""

    @admin.action(description="Clear Inventory")  # --> action button
    def clear_inventory(self, request, queryset):
        update_query = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_query} products were updated.',  # show the message to the user
            messages.ERROR
        )

    class Meta:
        model = models.Product


@admin.register(models.Customer)  # using annotation to register
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']  # 'orders_count'
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name']
    search_fields = ['first_name__istartswith']

    """def order(self, customer):
        urls = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
                    'customer__id': customer.id
                })
        )
        return format_html('<a href={}> {} </a>',
                           urls,
                           customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('orders'))"""

    class Meta:
        model = models.Customer


# inline
class OrderItemInline(admin.TabularInline):  # TabularInline --> table format , StackedInline --> stack format
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
    list_per_page = 10
    fields = ['payment_status', 'customer']  # 'placed_at' --> to include the date remove the auto date

    class Meta:
        model = models.Order

# admin.site.register(models.Collection, CollectionAdmin) # using method to register
# admin.site.register(models.Product, ProductAdmin) # using method to register
