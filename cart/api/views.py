from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView

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
        return Cart.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)


class CartDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = None

    def post(self, request, *args, **kwargs):
        CartItem.objects.filter(cart__user=self.request.user).filter(
            product__id__in=request.data
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
