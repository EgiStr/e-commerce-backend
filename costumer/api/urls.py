
from django.urls import path

from .views import (
    LoginView,
    DashbordView,
    LogoutView,
    RefreshTokenView,
    RegisterUserApiView)

from store.api.views import BookMarkUserApiView

urlpatterns = [
    # user detail
    path('',DashbordView.as_view(),name="dashboard"),
    path("bookmark/", BookMarkUserApiView.as_view(), name=""),

    # auth system router
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path("register/", RegisterUserApiView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
