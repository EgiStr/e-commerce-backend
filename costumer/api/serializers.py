from order.api.serializers import OrderSeriliazer
from costumer.models import Location, Store
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions, serializers

from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class registeruser(ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[
                UniqueValidator(queryset=User.objects.all(),message='Email already use'),
            ]
    )
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','username', 'password', 'password2' )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"email": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        
        try:
            email_valid = validated_data['email']

        except:
            raise serializers.ValidationError({"email": "email required !"})
        
        user = User.objects.create(
            username=validated_data['username'],
            email=email_valid,
        )

        user.set_password(validated_data['password'])
        
        user.save()

        return user

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'geolocation',
            'city',
            'address',
        ]

class UserDetailSerilaizer(ModelSerializer):
    location = SerializerMethodField()
    order_history = SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'profile',
            'phone',
            'location',
            'order_history'
        ]
    
    def get_location(self,obj):
        qs = obj.get_location()
        return LocationSerializer(qs,many=True).data
    
    def get_order_history(self,obj):
        return OrderSeriliazer(obj.get_order_history(),many=True).data


class UserEditProfilSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'profile',
            'phone',
        ]

class StoreproductDetailSerializer(ModelSerializer):
    location = SerializerMethodField()
    count_product = SerializerMethodField()

    class Meta:
        model = Store
        fields = (
            'name',
            'location',
            'count_product'
        )
    
    def get_location(self,obj):
        try:
            qs = obj.get_location().first()
            return LocationSerializer(qs).data
        except Exception as e :
            return 
    
    def get_count_product(self,obj):
        qs = obj.get_product().count()
        return qs