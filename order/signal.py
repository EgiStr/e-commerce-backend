from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Order, OrderItem
from costumer.models import TokenNotif

from utils.firebase.sendnotif import (
    send_notif_device,
    send_notif_multiple,
    registerToken,
)


@receiver(post_save, sender=Order)
def OrderCreate(instance, created, *args, **kwargs):
    if instance.order_status == "delivery":
        orders = instance.get_order_item()
        for order in orders:
            varian = order.product
            product = varian.product
            # receive = product.penjual
            # for real product
            # token = TokenNotif.objects.filter(user=receive)
            # tokens = [qs.token for qs in token]
            image = instance.get_thumb().image.url
            data = {
                "image": image,
                "title": f"{product.title} varian {varian.name}",
                "type": "order",
            }
        send_notif_multiple(
            [
                "djh4QzIBzm8Dcy2Qt0njOH:APA91bHH0xhrhaEFpwHdgZ0syKM6XV7_d4GeoEVzJOEH7S-uLPQkxrA6DP8NBpNUHxq0qRfID5FPie9SEh9MEBN4aWDT1di3TUa8HMPkykdpcqg4ozdsaRFhf8mMa2Cl2CObrJdXlqGJ"
            ],
            data,
            title="you must send product in 7 day",
        )

        # send_notif_multiple([registerToken],data)


@receiver(post_save, sender=OrderItem)
def NotifOrder(instance, created, *args, **kwargs):
    if created:
        varian = instance.product
        product = varian.product
        # receive = product.penjual
        # for real product
        # token = TokenNotif.objects.filter(user=receive)
        # tokens = [qs.token for qs in token]
        image = instance.get_thumb().image.url
        data = {
            "image": image,
            "title": f"{product.title} varian {varian.name}",
            "type": "order",
        }
        send_notif_multiple(
            [
                "djh4QzIBzm8Dcy2Qt0njOH:APA91bHH0xhrhaEFpwHdgZ0syKM6XV7_d4GeoEVzJOEH7S-uLPQkxrA6DP8NBpNUHxq0qRfID5FPie9SEh9MEBN4aWDT1di3TUa8HMPkykdpcqg4ozdsaRFhf8mMa2Cl2CObrJdXlqGJ"
            ],
            data,
        )


# @receiver(post_save,sender=Varian)
# def Variancreate(instance,created,*args, **kwargs):
#     product = instance.product
#     product.price = product.get_price
#     product.save()


@receiver(post_delete, sender=Order)
def OrderDelete(instance, *args, **kwargs):
    orders = instance.get_order_item()
    for order in orders:
        varian = order.product
        product = varian.product
        # receive = product.penjual
        # for real product
        # token = TokenNotif.objects.filter(user=receive)
        # tokens = [qs.token for qs in token]
        image = instance.get_thumb().image.url
        data = {
            "image": image,
            "title": f"{product.title} varian {varian.name}",
            "type": "order",
        }
        send_notif_multiple(
            [
                "djh4QzIBzm8Dcy2Qt0njOH:APA91bHH0xhrhaEFpwHdgZ0syKM6XV7_d4GeoEVzJOEH7S-uLPQkxrA6DP8NBpNUHxq0qRfID5FPie9SEh9MEBN4aWDT1di3TUa8HMPkykdpcqg4ozdsaRFhf8mMa2Cl2CObrJdXlqGJ"
            ],
            data,
            title="upss !, order cancel",
        )
