from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver

from django.utils.text import slugify
from .models import Product,Category,Varian


# reset password


@receiver(pre_save,sender=Product)
def productUpdate(instance,*args, **kwargs):
  instance.slug= slugify(instance.title)

@receiver(post_save,sender=Product)
def Productcreate(instance,created,*args, **kwargs):
    if created:
      instance.slug = slugify(instance.title)
      instance.save()

@receiver(post_save,sender=Varian)
def Variancreate(instance,created,*args, **kwargs):
    product = instance.product
    product.price = product.get_price
    product.save()

@receiver(post_save,sender=Category)
def Productcreate(instance,created,*args, **kwargs):
    if created:
      instance.slug=slugify(instance.content)
      instance.save()
