from costumer.api.serializers import UserNotifSerializer
from rest_framework.serializers import ModelSerializer,SerializerMethodField,Serializer

from notification.models import Notifikasi

class NotifSerializer(ModelSerializer):
    # post = SerializerMethodField()
    sender = SerializerMethodField()
    create_at = SerializerMethodField()
    
    class Meta:
        model =  Notifikasi
        fields = [
            # 'post',
            'id',
            'sender',
            'create_at',
            'type_notif',
            'more_text',
            'is_seen'
        ]

    def get_create_at(self,obj):
        return obj.get_create_time
    
    def get_sender(self,obj):
        return UserNotifSerializer(obj.sender).data

    # def get_post(self,obj):
    #     # ngecek ada post ga ?
    #     try:
    #         obj.post.url
    #     except:
    #         return None
    #     return obj.post.url

