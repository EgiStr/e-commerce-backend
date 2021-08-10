from costumer.models import Location
from django.db import models
from django.conf import settings

from store.models import Varian
# Create your models here.

class Order(models.Model):
    ORDER_STATUS = (
        ('payment','payment'),
        ('delivery',"delivery"),
        ('finish',"finish"),
        ('cancel',"cancel"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order", on_delete=models.CASCADE)
 
    ongkir = models.IntegerField(blank=True, null=True)
    order_key = models.CharField(unique=True,max_length=70)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default='payment')
    paid = models.BooleanField(default=False) # True berarti sudah bayar

    create_at = models.DateTimeField(auto_now=False, auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-create_at',)

    def __str__(self):
        return f"order {self.user.username} at {self.create_at}"
    
    @property
    def get_total_paid(self):
        return sum(item.get_total_price for item in self.order_item.all())
    
    @property
    def get_total_item(self):
        return sum(item.quantity for item in self.order_item.all())

    def get_order_item(self):
        return self.order_item.all()
    
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Varian, related_name="product_order",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) :
        return self.product.product.title
    
    @property
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def get_product(self):
        return self.product
    
    def get_thumb(self):
        qs = self.product.get_image_varian()
        return qs or self.product.product.get_thumb()


