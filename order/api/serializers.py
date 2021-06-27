from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from order.models import Order, OrderItem

from store.api.serializers import ProductOrderSerializer
import uuid
from django.db import transaction


class OrderItemCreateSerializers(ModelSerializer):
    quantity = serializers.IntegerField(default=1)
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), required=False, allow_null=True, default=None
    )

    class Meta:
        model = OrderItem
        fields = [
            "quantity",
            "product",
            "order",
        ]

    def create(self, validated_data):
        quantity = validated_data.pop("quantity")
        order = validated_data.pop("order")
        user = validated_data.pop("user")

        if order:
            orderItem = OrderItem.objects.get(order=order, **validated_data)
        else:
            orderQs = Order.objects.create(user=user, order_key=str(uuid.uuid4())[:12])
            orderItem = OrderItem.objects.create(order=orderQs, **validated_data)

        if quantity == 0:
            orderItem.delete()
            return validated_data

        orderItem.quantity = quantity
        orderItem.save()

        return orderItem


class OrderitemEditSerializer(ModelSerializer):
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderItemSerialiazer(ModelSerializer):

    product = ProductOrderSerializer()

    class Meta:
        model = OrderItem
        fields = ['id','product','quantity']
    
class OrderSeriliazer(ModelSerializer):

    total_paid = SerializerMethodField()
    total_item = SerializerMethodField()
    order_item = OrderItemSerialiazer(many=True)

    class Meta:
        model = Order
        fields = [
            "create_at",
            "order_status",
            "order_key",
            "total_paid",
            "total_item",
            "order_item",
        ]

    def get_total_paid(self, obj):
        return obj.get_total_paid

    def get_total_item(self, obj):
        return obj.get_total_item

  
class OrderCreateSeriliazer(ModelSerializer):
    order_item = OrderitemEditSerializer(many=True)

    class Meta:
        model = Order
        # fields = ['order_items']
        fields = ["id", "order_key", "order_item", "location"]

    def create(self, validated_data):
        order_items = validated_data.pop("order_item")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            order_item = []
            for item in order_items:
                varian_product = item.get("product")
                product = varian_product.product

                if varian_product.stock < item.get("quantity"):
                    raise serializers.ValidationError(
                        {"message": "you quantity beyond stock product "}
                    )

                # update stock and sold product
                varian_product.stock = varian_product.stock - item.get("quantity")
                varian_product.save()
                product.sold = product.sold + item.get("quantity")
                product.save()

                order_item.append(OrderItem(order=order, **item))
            OrderItem.objects.bulk_create(order_item)

        return order


class OrderDetailSerializer(ModelSerializer):
    total_paid = SerializerMethodField()
    total_item = SerializerMethodField()
    order_item = SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total_paid(self, obj):
        return obj.get_total_paid

    def get_total_item(self, obj):
        return obj.get_total_item

    def get_order_item(self, obj):
        return OrderItemSerialiazer(obj.get_order_item(), many=True).data


class OrderUpdateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_status",
            "paid",
        ]

    def update(self, instance, validated_data):
        instance.order_status = validated_data.get(
            "order_status", instance.order_status
        )
        instance.paid = validated_data.get("paid", instance.paid)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     order_items = validated_data.pop('order_item')
    #     order_item = list((instance.order_item).all())

    #     for order_i in order_items:
    #         try:
    #             item = order_item.pop(0)
    #             if item.product.stock < order_i.get('quantity',item.quantity):
    #                 raise serializers.ValidationError({"message" : "you quantity beyond stock product "})

    #             item.quantity = order_i.get('quantity',item.quantity)
    #             item.save()

    #         except IndexError:
    #             OrderItem.objects.create(order=instance,**order_i)
    #     """
    #         for update except image
    #         and user can append varian
    #         note "user cant delete but can unactive varian == delete"
    #     """

    #     return instance
