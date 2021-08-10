from django.urls import path

from .views import OrderApiView,OrderDetailApiView,OrderPaymentApiView
urlpatterns = [
    path("", OrderApiView.as_view(), name="order-create"),
    path("<str:order_key>/", OrderDetailApiView.as_view(), name="detail"),
    path("<int:pk>/payment/", OrderPaymentApiView.as_view(), name="payment"),
]
