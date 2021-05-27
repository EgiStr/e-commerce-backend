from rest_framework import status
from rest_framework.generics import DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin

from .serializers import CartListSerializer, CartItemCreateSerializer
from .permissions import IsCartAuth

from cart.models import Cart, CartItem


class CartApiView(CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CartItemCreateSerializer
        return CartListSerializer

    def get_queryset(self):
        qs = Cart.objects.get(user=self.request.user)
        return qs

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)


class CartDeleteApiView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCartAuth]

    def get_queryset(self):
        return CartItem.objects.filter(id=self.kwargs["pk"])
