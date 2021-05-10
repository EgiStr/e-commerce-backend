
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from store.models import Bookmark, Image, Product, Rating, Varian ,Category
from costumer.api.serializers import StoreproductDetailSerializer

class CategorySerialiazer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['content']
    

class imageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image',
            'is_thumb'
        ]

class VarianCreateSerializer(ModelSerializer):
    image = imageSerializer()
    class Meta:
        model = Varian
        fields = [
            'name',
            'stock',
            'price',
            'image',
        ]

class VarianSerializer(ModelSerializer):

    image = SerializerMethodField()

    class Meta:
        model = Varian
        fields = [
            'id',
            'name',
            'stock',
            'price',
            'image',
        ]
    
    def get_image(self,obj):
        return imageSerializer(obj.get_image_varian(),many=True).data

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'rating',
            'ulasan'
        ]

class ProductListSerializer(ModelSerializer):

    thumb = SerializerMethodField()
    store = SerializerMethodField()
    price = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'store',
            'title',
            'price',
            'slug',
            'sold',
            'thumb',
          
        ]

    def get_thumb(self,obj):
        try:
            imageSerializer(obj.get_thumb()).data
        except Exception as e :
            return 

    def get_price(self,obj):
        return obj.get_price
    
    def get_store(self,obj):
        return obj.penjual.name
    


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
            'store',
            'penjual',
            'category',
            'title',
            'desc',
            "is_active",
            'sold',
            'image',
            'rating',
            'rating_avg',
            'varian',
            'stock',
        ]
    
    def get_store(self,obj):
        data = StoreproductDetailSerializer(obj.penjual).data
        return data
    
    def get_image(self,obj):
        return imageSerializer(obj.get_image(),many=True).data

    def get_rating_avg(self,obj):
        return obj.get_rating_avg     
    
    def get_rating(self,obj):
        qs = obj.get_rating()
        return RatingSerializer(qs,many=True).data

    def get_varian(self,obj):
        return VarianSerializer(obj.get_varian(),many=True).data
    
    def get_stock(self,obj):
        return obj.get_stock

class ProductCreateSerializer(ModelSerializer):
    # buat fields costume buat varian, gambar, category dll
    category = serializers.CharField()
    image = imageSerializer(many=True)
    varian = VarianCreateSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'penjual',
            'title',
            'desc', 
            'category',
            'image',
            'varian', 
        ]
    
    def create(self, validated_data):

        category_data = Category.objects.get_or_create(content=validated_data.pop('category'))
        
        image_datas = validated_data.pop('image')
        varian_datas = validated_data.pop('varian')

        product = Product.objects.create(category=category_data,**validated_data)

        image = [Image(product=product.id,**image_data) for image_data in image_datas]

        # varian data / belum jalan
        for varian in varian_datas:
            if varian.image:
                obj_id = Varian.objects.create(name=varian.name ,stock=varian.stock, price=varian.price)
                image.append(Image(varian=obj_id,**varian.image))

        # data image
        Image.objects.bulk_create(image)
        

        return product


class ProductEditSerializer(ModelSerializer):
    varian = VarianCreateSerializer(many=True)
   
    class Meta:
        model = Product
        fields = [
            'title',
            'desc',
            'varian',
            # masih berpikir buat Edit Varian
        ]

    def update(self, instance, validated_data):
        varian_data = validated_data.pop('varian')
        varian = list((instance.varian).all())
    
        instance.title = validated_data.get('title', instance.title)
        instance.desc = validated_data.get('desc', instance.desc)

        instance.save()

        for v1 in varian_data:
            vr = varian.pop(0)
            vr.name = v1.get('name',vr.name)
            vr.stock = v1.get('stock',vr.stock)
            vr.price = v1.get('price',vr.price)
            vr.save()

        return instance



class RatingCreateSerializers(ModelSerializer):
    class Meta:
        model = Rating
        feidls = "__all__"

class RatingEditSerializers(ModelSerializer):
    class Meta:
        model = Rating
        feidls = ('ulasan','rating')

class BookMarkSerializer(ModelSerializer):
    class Meta:
        model= Bookmark
        fields = "__all__"
    
    def create(self, validated_data):
        qs_create,created =  Bookmark.objects.get_or_create(**validated_data)

        if created:
            return qs_create
        qs_create.delete()

        return validated_data
 