from django.db.models.query import Prefetch
from costumer.models import Location, Store
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from store.models import Bookmark, Category, Image, Product, Rating, Varian
from utils.serializers import Base64ImageField


class LocationStoreSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "city", "city_id"]


class StoreSerializer(ModelSerializer):
    location = LocationStoreSerializer(many=True)

    class Meta:
        model = Store
        fields = ["id", "name", "profile", "location"]


class CategorySerialiazer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["content"]


class imageSerializer(ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = Image
        fields = ["image", "is_thumb"]


class VarianCreateSerializer(ModelSerializer):
    image = imageSerializer()

    class Meta:
        model = Varian
        fields = [
            "name",
            "stock",
            "price",
            "image",
        ]


class VarianEditSerializer(ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Varian
        fields = ["name", "stock", "price", "is_active"]


class VarianSerializer(ModelSerializer):

    image = SerializerMethodField()

    class Meta:
        model = Varian
        fields = [
            "id",
            "name",
            "stock",
            "price",
            "image",
        ]

    def get_image(self, obj):
        try:
            return imageSerializer(obj.get_image_varian(), many=True).data
        except Exception as e:
            return imageSerializer(obj.get_image_varian()).data


class RatingSerializer(ModelSerializer):
    username = SerializerMethodField()
    profile = SerializerMethodField()

    class Meta:
        model = Rating
        fields = [
            "username",
            "profile",
            "create_at",
            "rating",
            "ulasan",
        ]

    def get_username(self, obj):
        return obj.user.username

    def get_profile(self, obj):
        profile = obj.user.profile
        if profile.name != "":
            return f"media/{profile.name}"
        return None


# for order Product -> varian
class ProductOrderSerializer(ModelSerializer):
    title = SerializerMethodField()
    store = SerializerMethodField()
    slug = SerializerMethodField()
    varian = SerializerMethodField()
    thumb = SerializerMethodField()

    class Meta:
        model = Varian
        fields = [
            "id",
            "title",
            "varian",
            "store",
            "thumb",
            "price",
            "slug",
        ]

    def get_thumb(self, obj):
        try:
            qs = obj.get_image_varian()
            if qs == None:
                qs = obj.product.images
            return imageSerializer(qs).data
        except Exception:
            return imageSerializer(qs,many=True).data

    def get_varian(self, obj):
        return obj.name

    def get_title(self, obj):
        return obj.product.title

    def get_store(self, obj):
        return StoreSerializer(obj.product.penjual).data

    def get_slug(self, obj):
        return obj.product.slug

class ProductDashboardSerializer(ModelSerializer):
    varian = VarianSerializer(many=True)
    thumb = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','price','title','thumb','varian','sold']
    
    def get_thumb(self, obj):
        try:
            qs = imageSerializer(obj.get_image()[0])
            return qs.data
        except Exception as e:
            return None
class ProductListSerializer(ModelSerializer):

    thumb = SerializerMethodField()
    store = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "store", "title", "price", "slug", "sold", "thumb", "price"]

    def get_thumb(self, obj):
        try:
            qs = imageSerializer(obj.get_image()[0])
            return qs.data
        except Exception as e:
            return None

    def get_store(self, obj):

        return StoreSerializer(obj.penjual).data

    @classmethod
    def eager_loading(cls, queryset):
        queryset = queryset.prefetch_related(
            Prefetch(
                "penjual",
                queryset=Store.objects.prefetch_related("location"),
            )
        ).prefetch_related(
            Prefetch("images", queryset=Image.objects.filter(is_thumb=True))
        )
        return queryset


class ProductDetailSerializer(ModelSerializer):

    image = SerializerMethodField()
    rating = SerializerMethodField()
    store = SerializerMethodField()
    rating_avg = SerializerMethodField()
    varian = SerializerMethodField()
    stock = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "store",
            "slug",
            "penjual",
            "category",
            "title",
            "desc",
            "is_active",
            "sold",
            "image",
            "rating",
            "rating_avg",
            "varian",
            "stock",
        ]

    def get_store(self, obj):

        return StoreSerializer(obj.penjual).data

    def get_image(self, obj):
        try:
            return imageSerializer(obj.get_image(), many=True).data
        except Exception as e:
            return imageSerializer(obj.get_image()).data

    def get_rating_avg(self, obj):
        return obj.get_rating_avg

    def get_rating(self, obj):
        qs = obj.get_rating()[:10]
        return RatingSerializer(qs, many=True).data

    def get_varian(self, obj):
        return VarianSerializer(obj.get_varian(), many=True).data

    def get_stock(self, obj):
        return obj.get_stock

    @classmethod
    def eager_loading(cls, queryset):
        queryset = queryset.prefetch_related(
                Prefetch(
                    "penjual",
                    queryset=Store.objects.prefetch_related("location"),
                )
            ).prefetch_related(
                Prefetch("images", queryset=Image.objects.all())
            ).prefetch_related(
                Prefetch("rating", queryset=Rating.objects.select_related("user"))
            ).prefetch_related(
                Prefetch("varian", queryset=Varian.objects.prefetch_related('image_varian'))
            )
        
        return queryset


class ProductCreateSerializer(ModelSerializer):
    # buat fields costume buat varian, gambar, category dll
    category = serializers.CharField()
    image = imageSerializer(many=True, write_only=True)
    varian = VarianCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "desc",
            "category",
            "image",
            "varian",
        ]

    def create(self, validated_data):
        # print(validated_data.pop('category'))

        category_data, created = Category.objects.get_or_create(
            content=validated_data.pop("category")
        )  # for create new one or use

        """ 
            pop data exclude product data
        """
        image_datas = validated_data.pop("image")
        varian_datas = validated_data.pop("varian")

        product, created_product = Product.objects.get_or_create(
            category=category_data, **validated_data
        )

        # check if already create same title
        if not created_product:
            raise serializers.ValidationError(
                {"title": f" you already have title get other title "}
            )

        # create image table use trick bulk_create for optimaze
        image = []
        for i, image_data in enumerate(image_datas):
            # for create thumb if first image
            if i == 0:
                image.append(
                    Image(product=product, image=image_data.get("image"), is_thumb=True)
                )
            else:
                image.append(Image(product=product, **image_data))

        # create varian
        for varian in varian_datas:
            varian = dict(varian)
            obj_id = Varian.objects.create(
                product=product,
                name=varian.get("name"),
                stock=varian.get("stock"),
                price=varian.get("price"),
            )

            image.append(Image(varian=obj_id, **varian.get("image")))

        # data image
        Image.objects.bulk_create(image)

        return product


class ProductEditSerializer(ModelSerializer):
    varian = VarianEditSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "desc",
            "varian",
            # masih berpikir buat Edit Varian
        ]

    def update(self, instance, validated_data):
        varian_data = validated_data.pop("varian")
        varian = list((instance.varian).all())

        instance.title = validated_data.get("title", instance.title)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.save()

        """
            for update except image
            and user can append varian
            note "user cant delete but can unactive varian == delete"
        """

        for v1 in varian_data:
            try:
                vr = varian.pop(0)
                vr.name = v1.get("name", vr.name)
                vr.stock = v1.get("stock", vr.stock)
                vr.price = v1.get("price", vr.price)
                vr.is_active = v1.get("is_active", vr.is_active)
                vr.save()

            except IndexError:
                Varian.objects.create(product=instance, **v1)

        return instance


class RatingCreateSerializers(ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

    def create(self, validated_data):
        instance, created = Rating.objects.get_or_create(**validated_data)

        if created:
            return instance

        raise serializers.ValidationError(
            {"message": f"you already rating {instance.rating} this product"}
        )


class RatingEditSerializers(ModelSerializer):
    class Meta:
        model = Rating
        fields = ("ulasan", "rating")

    def update(self, instance, validated_data):
        instance.ulasan = validated_data.get("ulasan", instance.ulasan)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.save()
        return instance


class BookMarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["product"]

    def create(self, validated_data):
        qs_create, created = Bookmark.objects.get_or_create(**validated_data)

        if created:
            return qs_create

        qs_create.delete()

        return validated_data
