
from django.urls import path

from .views import (
    LoginView,
    DashbordView,
    LogoutView,
    RefreshTokenView,
    RegisterUserApiView,
    ChangePasswordApiView,
    StoreDashboard)

from store.api.views import BookMarkUserApiView

urlpatterns = [
    # user detail
    path('',DashbordView.as_view(),name="dashboard"),
    path('store/',StoreDashboard.as_view(),name="store-dashboard"),
    path("bookmark/", BookMarkUserApiView.as_view(), name="bookmark"),
    
    # auth system router
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path("register/", RegisterUserApiView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
