from django.urls import path

from .views import sendMessageApiView

urlpatterns = [
    path('send/', sendMessageApiView,name='sendMessage'),
]
