from django.contrib import admin

# Register your models here.
from order.models import Cart, CartItem, Order, Address, OrderItem


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'total',
    ]


class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'cart',
        'book',
        'quantity',
        'price'
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'order_id',
        'order_at',
        'total',
        'status'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
        'line1',
        'line2',
        'city',
        'state',
        'zip',
        'contact'
    ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'subtotal',
    ]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
