from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from costumer.models import Store
# Create your models here.

class Category(models.Model):
    content = models.CharField(max_length=70)
    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.content

class Image(models.Model):
    product = models.ForeignKey('Product', related_name="images" ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', height_field='height_field', width_field='width_field')
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)

class Varian(models.Model):
    product = models.ForeignKey("Product",related_name="varian", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    penjual = models.ForeignKey(Store,related_name="product",  on_delete=models.CASCADE)
    category= models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    
    title = models.CharField(max_length=80)
    desc = models.TextField(max_length=300,blank=True, null=True)
    price = models.IntegerField(default=0)
    tumb = models.ImageField(upload_to='thumb',blank=True, null=True)

    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)
    sold = models.IntegerField(_("terjual "), default=0)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
        return f'product {self.penjual} title {self.title}'
        
    
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="rating" ,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  related_name="rating",on_delete=models.CASCADE)
    rating  = models.PositiveIntegerField(_(" rating"))
    ulasan = models.TextField(_(" review") , max_length=200)


    def __str__(self):
        return self.product.title
    