from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items', 'discount', 'tax')
    filter_horizontal = ('items',)

    def get_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])

    get_items.short_description = 'Items'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent_off', 'stripe_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'stripe_id')

# Register your models here.
