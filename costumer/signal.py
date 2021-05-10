from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


from .models import CustomUser,Store
from cart.models import Cart

# reset password

@receiver(post_save,sender=CustomUser)
def Cart_create(instance,created,*args, **kwargs):
    if created:
       Cart.objects.get_or_create(user=instance)
