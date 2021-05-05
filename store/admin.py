from django.contrib import admin
from django.utils.safestring import mark_safe
from store.models import (
                        Category,
                        Product,
                        Image,
                        Varian,
                        Rating)

class ImageInline(admin.TabularInline):
    model = Image
    fields = [
        'image',
        'is_thumb',
        
    ]
class VarianInline(admin.TabularInline):
    model = Varian
    fields = [
        'name',
        'stock',
        'is_active'
        
    ]
class RatingInline(admin.TabularInline):
    model = Rating

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'penjual',
        'stock',
        'rating'
    )
    list_filter = ("category", )

    readonly_fields = (
        'slug',
        'sold',
        'create_at',
        'update',
    )
    
    inlines = [ImageInline,VarianInline,RatingInline]

    def stock(self,obj):
        return obj.get_stock or 0
    
    def rating(self,obj):
        return obj.get_rating or 0

    
admin.site.register(Category)