from django.urls import path

from .views import (
    ProductApiView,
    productDetailAPiView,
    CategoryProductApiView,

)

urlpatterns = [
    path("", ProductApiView.as_view(), name="list-create"),
    path("category/<str:slug>/", CategoryProductApiView.as_view(), name="category"),
    path("<str:store>/<str:slug>/", productDetailAPiView.as_view(), name="detail"),
]
