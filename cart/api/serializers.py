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
        cartItem, created = CartItem.objects.get_or_create(**validated_data)   
        cartItem.quantity = quantity
        cartItem.save()
        varian_product=cartItem.product
     
        # validate stock if  quantity beyond stock
        if varian_product.stock < quantity:
            raise serializers.ValidationError({"message" : "you quantity beyond stock product "})

        return cartItem


class CartItemSerializer(ModelSerializer):

    # total_item = SerializerMethodField()
    product = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product','quantity']

   
    def get_product(self, obj):
        return ProductOrderSerializer(obj.product).data

    # def get_total_item(self, obj):
    #     return obj.total_price


class CartListSerializer(ModelSerializer):
    items = SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "items",
        ]

    def get_items(self, obj):
        return CartItemSerializer(obj.get_cart_item(), many=True).data
