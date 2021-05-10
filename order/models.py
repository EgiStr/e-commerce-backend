from django.db import models
from django.conf import settings

from store.models import Varian
# Create your models here.


class Order(models.Model):
    ORDER_STATUS = (
        ('payment','payment'),
        ('delivery',"delivery"),
        ('finish',"finist")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order", on_delete=models.CASCADE)
    total_paid = models.IntegerField(blank=True, null=True)
    order_key = models.CharField(unique=True,max_length=70)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS,default='payment')
    
    paid = models.BooleanField(default=False) # True berarti sudah bayar

    create_at = models.DateTimeField(auto_now=False, auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-create_at',)

    def __str__(self):
        return f"order {self.user.username} at {self.create_at}"
    
    @property
    def get_total_paid(self):
        return sum(item.get_total_price for item in self.order_item.all())
    
    def get_order_item(self):
        return self.order_item.all()
    
    def save(self, *args, **kwargs):
       self.total_paid = self.get_total_paid
       super(Order, self).save(*args, **kwargs) # Call the real save() method
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Varian, related_name="product_order",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) :
        return self.product.title
    
    @property
    def get_total_price(self):
        return self.product.price * self.quantity


