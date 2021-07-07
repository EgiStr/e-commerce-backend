from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',include(('costumer.api.urls', 'costumer.api'),namespace="auth")),
    path("api/product/", include(('store.api.urls','store.api'),namespace="product")),
    path("api/cart/", include(('cart.api.urls','cart.api'),namespace="cart")),
    path("api/order/", include(('order.api.urls','order.api'),namespace="order")),
    path("api/notification/", include(('notification.api.urls','notification.api'),namespace="notification")),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
