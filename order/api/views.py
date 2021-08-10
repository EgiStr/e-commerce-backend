from django.db.models.query import Prefetch
from utils.logSql import sql_logger
from order.api.permissions import IsOwner
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (
    OrderDetailSerializer,
    OrderSeriliazer,
    OrderCreateSeriliazer,
    OrderUpdateSerializer,
)
from order.models import Order
from store.api.paginations import PagePagination


class OrderApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PagePagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "order_status",
    ]  # dll

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        queryset = OrderSeriliazer.setup_eager_loading(queryset)
        return queryset 

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSeriliazer
        return OrderSeriliazer

   
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailApiView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "order_key"

    def get_serializer_class(self):
        return OrderDetailSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        queryset = self.get_serializer().setup_eager_loading(queryset)
        return queryset
        

    def delete(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs.update(order_status="cancel")
        return Response({"massage": "OrderCancel"})


class OrderPaymentApiView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderUpdateSerializer

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs["pk"])
