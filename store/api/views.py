from django.db.models import query
from costumer.models import Store
from rest_framework.permissions import  IsAuthenticated

from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView,RetrieveUpdateDestroyAPIView

from rest_framework.filters import SearchFilter,OrderingFilter

from store.api.serializers import (
    BookMarkSerializer,
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductEditSerializer,
    ProductListSerializer,
    RatingCreateSerializers,
    RatingEditSerializers,
    VarianCreateSerializer,

)

from store.api.permissions import IsAuthorOrReadonly,IsRatingAuthor
from store.api.paginations import PagePagination

from store.models import Bookmark, Product, Rating

class CategoryProductApiView(ListAPIView):

    pagination_class = PagePagination
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.select_related('category').filter(category__slug=self.kwargs['slug'])
        return qs


class ProductApiView(ListCreateAPIView):
    pagination_class = PagePagination
    
    filter_backends = [SearchFilter,OrderingFilter]
    
    ordering_fields = ['price','create_at','sold']
    search_fields = ['title','category__content','penjual__name']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        return ProductListSerializer.eager_loading(Product.objects.all())

    def perform_create(self, serializer):
        store = Store.objects.get(pemilik=self.request.user)
        serializer.save(penjual=store)
    
class productDetailAPiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadonly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method != 'GET':
            return ProductEditSerializer
        return ProductDetailSerializer

    def get_queryset(self):
        qs = Product.objects.filter(penjual__name=self.kwargs['store'],slug=self.kwargs['slug'])
        return ProductDetailSerializer.eager_loading(qs)
    
class VarianApiView(CreateAPIView):
    serializer_class = VarianCreateSerializer
    queryset = None

class BookMarkUserApiView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookMarkSerializer
        return ProductListSerializer

    def get_user_auth(self):
        return self.request.user
    
    def get_queryset(self):
        qs = Bookmark.objects.filter(user = self.get_user_auth())
        qs = [q.product for q in qs ]
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingCreateApiView(CreateAPIView):
    
    serializer_class = RatingCreateSerializers
    queryset = None
    permission_classes = [IsAuthenticated]

class RatingApiView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated,IsRatingAuthor]
    serializer_class = RatingEditSerializers

    def get_queryset(self):
        return Rating.objects.filter(id=self.kwargs['pk'])

    
