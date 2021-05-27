from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from cart.models import Cart, CartItem

from store.api.serializers import ProductOrderSerializer


class CartItemCreateSerializer(ModelSerializer):
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
        ]

    def create(self, validated_data):
        quantity = validated_data.pop("quantity")
        cartItem, created = CartItem.objects.get_or_create(quantity=quantity,**validated_data)   
        varian_product=cartItem.product
     
        # validate stock if  quantity beyond stock
        if varian_product.stock < quantity:
            raise serializers.ValidationError({"message" : "you quantity beyond stock product "})

        return cartItem


class CartItemSerializer(ModelSerializer):

    total_item = SerializerMethodField()
    detail_product = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_detail_product(self, obj):
        return ProductOrderSerializer(obj.product).data

    def get_total_item(self, obj):
        return obj.total_price


class CartListSerializer(ModelSerializer):
    items = SerializerMethodField()
    total_paid = SerializerMethodField()
    total_cart = SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "total_paid",
            "total_cart",
            "items",
        ]

    def get_items(self, obj):
        return CartItemSerializer(obj.get_cart_item(), many=True).data

    def get_total_paid(self, obj):
        return obj.get_total_paid

    def get_total_cart(self, obj):
        return obj.get_total_cart