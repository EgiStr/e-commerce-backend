from django.urls import path

from .views import (
    LocationApiView,
    LocationDatailApiView,
    LoginView,
    DashbordView,
    LogoutView,
    RefreshTokenView,
    RegisterUserApiView,
    ChangePasswordApiView,
    StoreDashboardApiView,
    WhoamiApiView,
    TokenApiView,
    AddressIndoApiView,
    CekOngkir
)

from store.api.views import BookMarkUserApiView

urlpatterns = [
    # user detail
    path("", DashbordView.as_view(), name="dashboard"),
    path("whoiam/", WhoamiApiView.as_view(), name="whoami"),
    path("token/", TokenApiView.as_view(), name="tokenNotif"),
    path("store/", StoreDashboardApiView.as_view(), name="store-dashboard"),
    path("bookmark/", BookMarkUserApiView.as_view(), name="bookmark"),
    path("location/", LocationApiView.as_view(), name="location"),
    path("location/<int:pk>/", LocationDatailApiView.as_view(), name="location-detail"),
    path("location/address/", AddressIndoApiView.as_view(), name="address-indonesia"),
    path("cek-ongkir/", CekOngkir.as_view(), name="cek-ongkir"),
    
    
    # auth system router
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterUserApiView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
]
