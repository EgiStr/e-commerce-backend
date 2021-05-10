from rest_framework.serializers import ModelSerializer,SerializerMethodField

from order.models import Order, OrderItem


class OrderItemSerialiazer(ModelSerializer):
    
    total_paid = SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
           'quantity',
           'total_paid',
           # tambahan product serializer # proses !   
        ]
    
    def get_total_paid(self,obj):
        return obj.get_total_price

class OrderSeriliazer(ModelSerializer):

    total_paid = SerializerMethodField()
    order_item = SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [

            'create_at',
            'order_status',
            'order_key',
            'total_paid',
            'order_item',
        ]
    
    def get_total_paid(self,obj):
        return obj.get_total_paid

    def get_order_item(self,obj):
        return OrderItemSerialiazer(obj.get_order_item(),many=True).data
    