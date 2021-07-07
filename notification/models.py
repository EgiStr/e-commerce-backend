from django.db import models
from django.conf import settings
from django.contrib.humanize.templatetags import humanize

# Create your models here.
from store.models import Product


class Notifikasi(models.Model):
    # TODO: Define fields here
    NOTIF_CHOIECE = (
        (1,'Order'),
        (2,'Massage'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product",blank=True, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender",related_query_name="pengirim")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_query_name="receiver",related_name="penerima")
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    type_notif = models.PositiveIntegerField(choices=NOTIF_CHOIECE)
    more_text = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create_at']

    def __str__(self):
       return f'notif {self.sender.username} for  {self.receiver} notif {self.type_notif}'

    # TODO: Define custom methods here

    @property
    def get_create_time(self):
        return humanize.naturalday(self.create_at)
