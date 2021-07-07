from django.urls import path

from notification.api.views import UserNotifikasiApiView



urlpatterns = [
    path('',UserNotifikasiApiView.as_view(),name="user-notif"),
]
