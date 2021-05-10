
from django.urls import path

from .views import (
    LoginView,
    DashbordView,
    LogoutView,
    RefreshTokenView,
    RegisterUserApiView)

urlpatterns = [
    path('',DashbordView.as_view(),name="dashboard"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path("register/", RegisterUserApiView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
