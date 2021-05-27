from django.contrib import admin

# Register your models here.
from order.models import Order,OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('quantity' ,'product' ,'total_paid' )
    readonly_fields = ('total_paid',)
    extra = 1
    
    def total_paid(self,obj):
        return obj.get_total_price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'total_paid',
        'order_key',
        "order_status"   
    )
    readonly_fields = (
        'total_paid',
        'order_status',
        'paid',
        'create_at',
        'updated',
    )
    
    inlines = [OrderItemInline]

    def total_paid(self,obj):
        return obj.get_total_paid or 0

    

@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity'
    )
    