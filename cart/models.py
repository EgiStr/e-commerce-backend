from django.db import models

from django.conf import settings
# Create your models here.

from store.models import Varian
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cart_user",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return f" cart user {self.user.username}"

    @property
    def get_total_cart(self):
        return self.cart_item.count()
    
    @property
    def get_total_paid(self):
        return sum(item.total_price for item in self.cart_item.all())
    
    def get_cart_item(self):
        return self.cart_item.all()

class CartItem(models.Model):
    product = models.ForeignKey(Varian, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name="cart_item",on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True, null=True) # fitur diskon

    # total harga ( bisa ditambah fitur diskon )
    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return " -  " + self.cart.user.username + "  cart_item"