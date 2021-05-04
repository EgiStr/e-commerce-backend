from django.contrib import admin

# Register your models here.
from costumer.models import CustomUser,Store

admin.site.register(CustomUser)
admin.site.register(Store)