from datetime import datetime

from django.db.models.query import Prefetch
from order.models import Order, OrderItem
from store.api.serializers import ProductListSerializer, StoreSerializer
from costumer.models import Location, Store, TokenNotif
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from order.api.serializers import OrderInvoiceSerilazer, OrderSeriliazer
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)
from rest_framework.validators import UniqueValidator
from utils.serializers import Base64ImageField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


class UserNotifSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "profile", "phone"]


class TokenSerializer(ModelSerializer):
    class Meta:
        model = TokenNotif
        fields = ["token"]

    def create(self, validated_data):
        token = TokenNotif.objects.get_or_create(**validated_data)
        return token


class registeruser(ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Email already use"),
        ],
    )
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):

        try:
            email_valid = validated_data["email"]

        except:
            raise serializers.ValidationError({"email": "email required !"})

        user = User.objects.create(
            username=validated_data["username"],
            email=email_valid,
        )

        user.set_password(validated_data["password"])

        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    new_password2 = serializers.CharField(required=True)


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "phone",
            "city",
            "city_id",
            "address",
            "postal_code",
            "other",
            "name_location",
            "type",
        ]


class LocationCreateSerializer(ModelSerializer):
    type = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "phone",
            "city",
            "city_id",
            "postal_code",
            "address",
            "other",
            "name_location",
            "store",
            "user",
            "type",
        ]

    def create(self, validated_data):
        user = validated_data.pop("user", None)
        store = validated_data.pop("store", None)
        if not user and store:
            raise serializers.ValidationError({"error": "error input"})
        if user:
            location = Location.objects.get_or_create(
                user=user, type="costumer", **validated_data
            )
        if store:
            location = Location.objects.get_or_create(
                store=store, type="store", **validated_data
            )

        return location[0]


class LocationEditSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "name",
            "phone",
            "city",
            "city_id",
            "address",
            "postal_code",
            "other",
            "name_location",
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.city_id = validated_data.get("city_id", instance.city_id)
        instance.address = validated_data.get("address", instance.address)
        instance.other = validated_data.get("other", instance.other)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)
        instance.name_location = validated_data.get(
            "name_location", instance.name_location
        )
        instance.save()
        return instance


class UserDetailSerilaizer(ModelSerializer):
    location = SerializerMethodField()
    order_history = SerializerMethodField()
    profile = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = User
        fields = ["email", "username", "profile", "phone", "location", "order_history"]

    def get_location(self, obj):
        qs = obj.get_location()
        return LocationSerializer(qs, many=True).data

    def get_order_history(self, obj):
        return OrderSeriliazer(obj.get_order_history(), many=True).data


class WhoamiSerializer(ModelSerializer):
    store = SerializerMethodField()
    location = SerializerMethodField()
    tokens = TokenSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "profile",
            "phone",
            "location",
            "store",
            "date_joined",
            "tokens",
        ]

    def get_store(self, obj):
        try:
            return StoreSerializer(obj.store).data
        except Exception:
            return None

    def get_location(self, obj):
        qs = obj.get_location()
        try:
            return LocationSerializer(qs, many=True).data
        except Exception:
            return LocationSerializer(qs).data


class UserEditProfilSerializer(ModelSerializer):
    profile = Base64ImageField(
        required=False, max_length=None, allow_empty_file=True, use_url=True
    )

    class Meta:
        model = User
        fields = ["username", "profile", "phone", "email"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.profile = validated_data.get("profile", instance.profile)
        instance.save()
        return instance


class summaryOrderSerialiazer(serializers.BaseSerializer):
    def sortPostalCode(self, query):
        data = {}
        for item in query:
            name = f"{item['city']}_{item['sub_district']}"

            if name in data:
                data[name] = [*data[name], item["postal_code"]]
            else:
                data[name] = [item["postal_code"]]
        return data

    def to_internal_value(self, data):
        return

    def to_representation(self, instance):
        orders = instance.get("order")
        total_orders = 0
        balance = 0
        salary = 0
        status_order = {}
        for item in list(orders):
            # for status order sort
            status = item.order_status
            if status in status_order:
                status_order[status] = status_order[status] + 1
            else:
                status_order[status] = 1
            balance += item.get_total_paid if status != "payment" else 0
            salary += item.get_total_item
            total_orders += 1

        return {
            "invoice": OrderInvoiceSerilazer(
                orders[:5],
                many=True,
            ).data,
            "summary": {
                "total_orders": total_orders,
                "balance": balance,
                "status": status_order,
                "salary": salary,
            },
        }

    @classmethod
    def setup_eager_loading(cls, queryset):
        queryset = queryset.prefetch_related(
            Prefetch("order_item", queryset=OrderItem.objects.select_related("product"))
        )
        return queryset


class StoreDetailSerializers(ModelSerializer):
    summary = SerializerMethodField()

    class Meta:
        model = Store
        fields = ["summary"]

    def get_summary(self, obj):
        order = Order.objects.filter(
            id__in=obj.get_order_id(), create_at__month=self.get_date()
        ).select_related("user")

        return summaryOrderSerialiazer(
            {"order": summaryOrderSerialiazer.setup_eager_loading(order)}
        ).data

    def get_date(self):
        return (
            self.context.get("date")
            if self.context.get("date")
            else datetime.today().month
        )


class UtilsOrderSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "count": instance.get("count", 0),
            "has_previous": instance.get("has_previous", False),
            "has_next": instance.get("has_next", False),
            "result": OrderInvoiceSerilazer(instance.get("orders", []), many=True).data,
        }

    def to_internal_value(self, data):
        return


class StoreOrdersSerializers(ModelSerializer):
    data = SerializerMethodField()

    class Meta:
        model = Store
        fields = [
            "data",
        ]

    def get_data(self, obj):
        order = Order.objects.filter(id__in=obj.get_order_id()).select_related("user")
        paginator = Paginator(order, 5)
        try:
            qs = paginator.page(self.get_page())
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)

        orders = {
            "orders": qs.object_list,
            "has_next": qs.has_next(),
            "has_previous": qs.has_previous(),
            "count": paginator.num_pages,
        }
        data = UtilsOrderSerializer(orders)
        # bakal diganti sama serializer yang baru
        return data.data

    def get_date(self):
        return (
            self.context.get("date")
            if self.context.get("date")
            else datetime.today().month
        )

    def get_page(self):
        return self.context.get("page", 1)


class UtilsProductSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            "count": instance.get("count", 0),
            "has_previous": instance.get("has_previous", False),
            "has_next": instance.get("has_next", False),
            "result": ProductListSerializer(
                instance.get("products"),
                many=True,
            ).data,
        }

    def to_internal_value(self, data):
        return


class StoreProductsSerializers(ModelSerializer):
    data = SerializerMethodField()

    class Meta:
        model = Store
        fields = ["data"]

    def get_data(self, obj):
        

        product = obj.get_product()
        paginator = Paginator(product, 5)
        try:
            qs = paginator.page(self.get_page())
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)
        product = {
            "products": qs.object_list,
            "has_next": qs.has_next(),
            "has_previous": qs.has_previous(),
            "count": paginator.num_pages,
        }
        return UtilsProductSerializer(product).data

    def get_date(self):

        return (
            self.context.get("date")
            if self.context.get("date")
            else datetime.today().month
        )

    def get_page(self):
        return self.context.get("page", 1)


class StoreproductDetailSerializer(ModelSerializer):
    location = SerializerMethodField()
    count_product = SerializerMethodField()

    class Meta:
        model = Store
        fields = ("name", "location", "count_product")

    def get_location(self, obj):
        try:
            qs = obj.get_location().first()
            return LocationSerializer(qs).data
        except Exception as e:
            return

    def get_count_product(self, obj):
        qs = obj.get_product().count()
        return qs
