from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.generics import ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from store.api.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductEditSerializer,
    ProductListSerializer,

)

from store.api.permissions import IsAuthorOrReadonly
from store.api.paginations import PagePagination
from store.models import Product

class CategoryProductApiView(ListAPIView):

    pagination_class = PagePagination
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category').filter(category__slug=self.kwargs['slug'])
        return qs


class ProductApiView(ListCreateAPIView):

    queryset= Product.objects.all()
    pagination_class = PagePagination

    def get_permission_classes(self):
        if self.request.method == "POST":
            return [IsAuthenticated,]
        return [AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer
    
class productDetailAPiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadonly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method != 'GET':
            return ProductEditSerializer,
        return ProductDetailSerializer

    def get_queryset(self):
        qs = Product.objects.filter(penjual__name=self.kwargs['store'],slug=self.kwargs['slug'])
        return qs
    