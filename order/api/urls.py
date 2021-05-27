from django.urls import path

from .views import OrderApiView,OrderDetailApiView,OrderPaymentApiView
urlpatterns = [
    path("", OrderApiView.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailApiView.as_view(), name="detail"),
    path("<int:pk>/payment/", OrderPaymentApiView.as_view(), name="payment"),
]
