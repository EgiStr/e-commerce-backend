from django.contrib.humanize.templatetags import humanize
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
from .models import Order, OrderItem
from costumer.models import TokenNotif
from notification.models import Notifikasi

from utils.firebase.sendnotif import (
    send_notif_device,
    send_notif_multiple,
    registerToken,
)


@receiver(post_save, sender=Order)
def OrderCreate(instance, created, *args, **kwargs):
    if instance.order_status == "delivery":
        notification = []
        orders = instance.get_order_item()
        # get all orderItem and looping
        for order in orders:
            varian = order.product
            product = varian.product
            receive = product.penjual.pemilik
            # for real product
            # get tokenNotif
            token = TokenNotif.objects.filter(user=receive)
            tokens = [qs.token for qs in token]
            image = instance.get_thumb().image.url
            data = {
                "image": image,
                "title": f"{product.title} varian {varian.name}",
                "type": "order",
            }

            send_notif_multiple(
                tokens,
                data,
                title="you must send product in 7 day",
            )
            deadline = datetime.datetime.now() + datetime.timedelta(days=7)
            notification.append(
                Notifikasi(sender=instance.user, receiver=receive, type_notif=1,more_text=f"you mush send product in {deadline.date()}")
            )

        # create notif
        Notifikasi.objects.bulk_create(notification)


@receiver(post_save, sender=OrderItem)
def NotifOrder(instance, created, *args, **kwargs):
    if created:

        varian = instance.product
        product = varian.product
        receive = product.penjual.pemilik
        # for real product
        token = TokenNotif.objects.filter(user=receive)
        tokens = [qs.token for qs in token]
        image = instance.get_thumb().image.url
        data = {
            "image": image,
            "title": f"{product.title} varian {varian.name}",
            "type": "order",
        }
        print(tokens)
        send_notif_multiple(
            tokens,
            data,
        )
        Notifikasi.objects.create(
            sender=instance.order.user, receiver=receive, type_notif=1,more_text=f"order {product.title} varian {varian.name}"
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
