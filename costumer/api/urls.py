
from django.urls import path

from .views import (
    LoginView,
    DashbordView,
    LogoutView,
    RefreshTokenView,
    RegisterUserApiView)

urlpatterns = [
    path('login/',LoginView.as_view(),name="login"),
    path("register/", RegisterUserApiView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('dashbord/',DashbordView.as_view(),name="dashboard")
]
