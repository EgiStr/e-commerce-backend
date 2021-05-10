from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.utils.text import slugify
from .models import Product,Category


# reset password

@receiver(post_save,sender=Product)
def Productcreate(instance,created,*args, **kwargs):
    if created:
      instance.slug=slugify(instance.title)
      instance.save()

@receiver(post_save,sender=Category)
def Productcreate(instance,created,*args, **kwargs):
    if created:
      instance.slug=slugify(instance.content)
      instance.save()
