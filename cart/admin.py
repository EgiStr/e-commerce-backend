from django.contrib import admin


# Register your models here.
from cart.models import Cart,CartItem

class OrderItemInline(admin.TabularInline):
    model = CartItem
    fields = ('quantity' ,'product' ,'total_paid' )
    readonly_fields = ('total_paid',)
    extra = 1
    
    def total_paid(self,obj):
        return obj.get_total_price


@admin.register(Cart)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'total_paid',
        "total_cart"   
    )
    readonly_fields = (
        'total_paid',
        'total_cart',
        'created_at',
        'updated',
    )
    
    inlines = [OrderItemInline]

    def total_paid(self,obj):
        return obj.get_total_paid or 0
    
    def total_cart(self,obj):
        return obj.get_total_cart or 0

    

@admin.register(CartItem)
class OrderItem(admin.ModelAdmin):
    list_display = (
        'cart',
        'product',
        'quantity'
    )
    