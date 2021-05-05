from django.contrib import admin

# Register your models here.
from costumer.models import CustomUser,Store,Location




class StoreInline(admin.TabularInline):
    model = Store

class LocationInline(admin.TabularInline):
    model = Location

@admin.register(CustomUser)
class CostumerAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
    )
   
    inlines = [StoreInline]

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
    
