from django.urls import path

from .views import (
    ProductApiView,
    productDetailAPiView,
    CategoryProductApiView,
    VarianApiView,
    RatingApiView,
    RatingCreateApiView
)

urlpatterns = [
    path("", ProductApiView.as_view(), name="list-create"),
    path("varian/", VarianApiView.as_view(), name="list-create"),
    path("rating/", RatingCreateApiView.as_view(), name="rating-create"),
    path("rating/<int:pk>/", RatingApiView.as_view(), name="rating-detail"),
   
    path("category/<str:slug>/", CategoryProductApiView.as_view(), name="category"),
    path("<str:store>/<str:slug>/", productDetailAPiView.as_view(), name="detail"),
]
