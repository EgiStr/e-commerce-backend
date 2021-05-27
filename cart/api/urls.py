from django.urls import path

from .views import CartApiView, CartDeleteApiView

urlpatterns = [
    path("", CartApiView.as_view(), name="cart"),
    path("<int:pk>/delete/", CartDeleteApiView.as_view(), name="cart-delete"),
    
]
