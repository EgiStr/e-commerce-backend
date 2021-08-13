from costumer.models import Store
from store.models import Image, Product, Varian
from django.db.models.query import Prefetch
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from cart.models import Cart, CartItem

from store.api.serializers import ProductOrderSerializer


class CartItemCreateSerializer(ModelSerializer):
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
        ]

    def create(self, validated_data):
        quantity = validated_data.pop("quantity")
        cartItem, created = CartItem.objects.get_or_create(**validated_data)
        cartItem.quantity = quantity
        cartItem.save()
        varian_product = cartItem.product

        # validate stock if  quantity beyond stock
        if varian_product.stock < quantity:
            raise serializers.ValidationError(
                {"message": "you quantity beyond stock product "}
            )

        return cartItem


class CartItemSerializer(ModelSerializer):

    product = SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def get_product(self, obj):
        return ProductOrderSerializer(obj.product).data


class CartListSerializer(ModelSerializer):
    items = SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "items",
        ]

    def get_items(self, obj):
        return CartItemSerializer(obj.cart_item, many=True).data

    @classmethod
    def eager_loading(cls, queryset):
        queryset = queryset.prefetch_related(
            Prefetch("cart_item", queryset=CartItem.objects.prefetch_related(
                    Prefetch(
                        "product",
                        queryset=Varian.objects.prefetch_related(
                            Prefetch(
                                "product",
                                queryset=Product.objects.prefetch_related(
                                    Prefetch(
                                        "penjual",
                                        queryset=Store.objects.prefetch_related(
                                            "location"
                                        ),
                                    )
                                
                                ).prefetch_related(Prefetch('images',queryset=Image.objects.filter(is_thumb=True))),
                            )
                        ).prefetch_related(
                            Prefetch(
                                "image_varian",
                                queryset=Image.objects.all(),
                            )
                        ),
                    )
                ))
        )
        return queryset[0]
